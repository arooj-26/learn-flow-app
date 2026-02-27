#!/usr/bin/env python3
"""
PostgreSQL Migration Runner

Executes pending database migrations with:
- Migration tracking in __migrations table
- Ordered execution (by filename)
- Rollback on failure
- Checksum verification

Usage:
    python run_migrations.py
    python run_migrations.py --dry-run
    python run_migrations.py --verbose

Exit Codes:
    0 - Success (migrations applied or none pending)
    1 - Failure (migration error)
"""

import argparse
import hashlib
import io
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
SCRIPT_DIR = Path(__file__).parent
MIGRATIONS_DIR = SCRIPT_DIR / "migrations"
LOG_FILE = SCRIPT_DIR / ".postgres-deploy.log"
CONNECTION_FILE = SCRIPT_DIR / ".connection"

# Migration file pattern: M001_description.sql, M002_another.sql, etc.
MIGRATION_PATTERN = re.compile(r'^M(\d{3})_.*\.sql$')


def log(level: str, message: str, verbose: bool = False):
    """Log message to file and optionally stdout."""
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    log_line = f"[{timestamp}] [{level}] {message}"

    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")
    except Exception:
        pass

    if verbose or level in ("ERROR", "INFO"):
        if level == "ERROR":
            print(log_line, file=sys.stderr)
        else:
            print(log_line)


def get_connection_params() -> dict:
    """Get database connection parameters."""
    params = {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": os.environ.get("POSTGRES_PORT", "5432"),
        "user": os.environ.get("POSTGRES_USER", "postgres"),
        "password": os.environ.get("POSTGRES_PASSWORD", ""),
        "database": os.environ.get("POSTGRES_DB", "learnflow"),
    }

    # Try to read from connection file
    if CONNECTION_FILE.exists():
        try:
            with open(CONNECTION_FILE) as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        env_key = key.upper()
                        if env_key == "POSTGRES_HOST":
                            params["host"] = value
                        elif env_key == "POSTGRES_PORT":
                            params["port"] = value
                        elif env_key == "POSTGRES_USER":
                            params["user"] = value
                        elif env_key == "POSTGRES_DB":
                            params["database"] = value
        except Exception:
            pass

    # Get password from kubectl if not set
    if not params["password"]:
        try:
            result = subprocess.run(
                ["kubectl", "get", "secret", "postgres-postgresql", "-n", "postgres",
                 "-o", "jsonpath={.data.postgres-password}"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                import base64
                params["password"] = base64.b64decode(result.stdout).decode()
        except Exception:
            pass

    return params


def get_connection_string(params: dict) -> str:
    """Build connection string from parameters."""
    return f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"


def calculate_checksum(filepath: Path) -> str:
    """Calculate MD5 checksum of a file."""
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def get_migration_files() -> List[Tuple[int, Path]]:
    """Get sorted list of migration files."""
    migrations = []

    if not MIGRATIONS_DIR.exists():
        return migrations

    for filepath in MIGRATIONS_DIR.iterdir():
        match = MIGRATION_PATTERN.match(filepath.name)
        if match:
            order = int(match.group(1))
            migrations.append((order, filepath))

    return sorted(migrations, key=lambda x: x[0])


def get_applied_migrations(params: dict) -> dict:
    """Get list of already applied migrations from database."""
    applied = {}

    try:
        import psycopg2

        conn = psycopg2.connect(
            host=params["host"],
            port=params["port"],
            user=params["user"],
            password=params["password"],
            database=params["database"],
            connect_timeout=10
        )

        cursor = conn.cursor()

        # Check if __migrations table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = '__migrations'
            )
        """)

        if cursor.fetchone()[0]:
            cursor.execute("SELECT migration_name, checksum FROM __migrations")
            for row in cursor.fetchall():
                applied[row[0]] = row[1]

        conn.close()

    except ImportError:
        log("ERROR", "psycopg2 not installed. Run: pip install psycopg2-binary")
        sys.exit(1)
    except Exception as e:
        log("DEBUG", f"Could not get applied migrations: {e}")

    return applied


def record_migration(params: dict, name: str, checksum: str, execution_time_ms: int) -> bool:
    """Record a migration as applied."""
    try:
        import psycopg2

        conn = psycopg2.connect(
            host=params["host"],
            port=params["port"],
            user=params["user"],
            password=params["password"],
            database=params["database"],
            connect_timeout=10
        )
        conn.autocommit = True

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO __migrations (migration_name, checksum, execution_time_ms)
            VALUES (%s, %s, %s)
            ON CONFLICT (migration_name) DO UPDATE SET
                checksum = EXCLUDED.checksum,
                applied_at = CURRENT_TIMESTAMP
        """, (name, checksum, execution_time_ms))

        conn.close()
        return True

    except Exception as e:
        log("ERROR", f"Failed to record migration: {e}")
        return False


def run_migration(params: dict, filepath: Path, verbose: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Run a single migration file.

    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    migration_name = filepath.stem  # e.g., "M001_add_users_table"

    try:
        import psycopg2

        # Read migration SQL
        with open(filepath, "r", encoding="utf-8") as f:
            sql = f.read()

        if not sql.strip():
            return True, None

        start_time = time.time()

        conn = psycopg2.connect(
            host=params["host"],
            port=params["port"],
            user=params["user"],
            password=params["password"],
            database=params["database"],
            connect_timeout=10
        )

        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            conn.commit()

            execution_time_ms = int((time.time() - start_time) * 1000)

            # Record migration
            checksum = calculate_checksum(filepath)
            record_migration(params, migration_name, checksum, execution_time_ms)

            log("INFO", f"Applied migration: {migration_name} ({execution_time_ms}ms)", verbose)

            return True, None

        except Exception as e:
            conn.rollback()
            error_msg = str(e)
            log("ERROR", f"Migration {migration_name} failed: {error_msg}", verbose)
            return False, error_msg

        finally:
            conn.close()

    except ImportError:
        return False, "psycopg2 not installed"
    except Exception as e:
        return False, str(e)


def ensure_migrations_table(params: dict) -> bool:
    """Ensure the __migrations tracking table exists."""
    try:
        import psycopg2

        conn = psycopg2.connect(
            host=params["host"],
            port=params["port"],
            user=params["user"],
            password=params["password"],
            database=params["database"],
            connect_timeout=10
        )
        conn.autocommit = True

        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS __migrations (
                id SERIAL PRIMARY KEY,
                migration_name VARCHAR(255) NOT NULL UNIQUE,
                applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                checksum VARCHAR(64),
                execution_time_ms INTEGER
            )
        """)

        conn.close()
        return True

    except Exception as e:
        log("ERROR", f"Failed to create migrations table: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run PostgreSQL migrations")
    parser.add_argument("--dry-run", action="store_true", help="Show pending migrations without applying")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    log("INFO", "Starting migration runner", args.verbose)

    # Get connection parameters
    params = get_connection_params()

    if not params["password"]:
        log("ERROR", "No database password found. Set POSTGRES_PASSWORD or ensure kubectl access.")
        print("[ERROR] Database password not found")
        sys.exit(1)

    # Ensure migrations table exists
    if not ensure_migrations_table(params):
        print("[ERROR] Could not create migrations table")
        sys.exit(1)

    # Get migration files
    migration_files = get_migration_files()

    if not migration_files:
        log("INFO", "No migration files found", args.verbose)
        print("[OK] No migrations to apply")
        sys.exit(0)

    # Get applied migrations
    applied = get_applied_migrations(params)

    # Find pending migrations
    pending = []
    for order, filepath in migration_files:
        migration_name = filepath.stem
        if migration_name not in applied:
            pending.append((order, filepath))
        else:
            # Check checksum mismatch
            current_checksum = calculate_checksum(filepath)
            if applied[migration_name] != current_checksum:
                log("WARN", f"Checksum mismatch for {migration_name}", args.verbose)

    if not pending:
        log("INFO", "No pending migrations", args.verbose)
        print("[OK] No pending migrations")
        sys.exit(0)

    log("INFO", f"Found {len(pending)} pending migration(s)", args.verbose)

    if args.dry_run:
        print(f"[DRY RUN] {len(pending)} pending migration(s):")
        for order, filepath in pending:
            print(f"  - {filepath.name}")
        sys.exit(0)

    # Apply migrations
    applied_count = 0
    failed_migration = None

    for order, filepath in pending:
        success, error = run_migration(params, filepath, args.verbose)

        if success:
            applied_count += 1
        else:
            failed_migration = (filepath.name, error)
            break

    # Report results
    if failed_migration:
        name, error = failed_migration
        log("ERROR", f"Migration failed: {name}", args.verbose)
        print(f"[ERROR] Migration {name} failed: {error}")
        print(f"[INFO] {applied_count} migration(s) applied before failure")
        sys.exit(1)
    else:
        log("INFO", f"Successfully applied {applied_count} migration(s)", args.verbose)
        print(f"[OK] {applied_count} migration(s) applied")
        sys.exit(0)


if __name__ == "__main__":
    main()
