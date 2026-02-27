#!/usr/bin/env python3
"""
PostgreSQL Backup Script

Creates pg_dump backups with:
- Gzip compression
- Timestamped filenames
- Backup directory management

Usage:
    python backup.py
    python backup.py --database learnflow
    python backup.py --output-dir /path/to/backups

Exit Codes:
    0 - Success
    1 - Failure
"""

import argparse
import gzip
import io
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
SCRIPT_DIR = Path(__file__).parent
DEFAULT_BACKUP_DIR = SCRIPT_DIR / "backups"
LOG_FILE = SCRIPT_DIR / ".postgres-deploy.log"
CONNECTION_FILE = SCRIPT_DIR / ".connection"
NAMESPACE = os.environ.get("NAMESPACE", "postgres")
RELEASE_NAME = os.environ.get("RELEASE_NAME", "postgres")


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
        print(log_line, file=sys.stderr if level == "ERROR" else sys.stdout)


def get_connection_params() -> dict:
    """Get database connection parameters."""
    params = {
        "host": os.environ.get("POSTGRES_HOST", f"{RELEASE_NAME}-postgresql.{NAMESPACE}.svc.cluster.local"),
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
                ["kubectl", "get", "secret", f"{RELEASE_NAME}-postgresql", "-n", NAMESPACE,
                 "-o", "jsonpath={.data.postgres-password}"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                import base64
                params["password"] = base64.b64decode(result.stdout).decode()
        except Exception:
            pass

    return params


def ensure_backup_dir(backup_dir: Path) -> bool:
    """Ensure backup directory exists."""
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        log("ERROR", f"Could not create backup directory: {e}")
        return False


def create_backup(params: dict, backup_dir: Path, verbose: bool = False) -> str:
    """
    Create a database backup.

    Returns:
        str: Path to backup file, or empty string on failure
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    database = params["database"]
    backup_filename = f"{database}_backup_{timestamp}.sql.gz"
    backup_path = backup_dir / backup_filename

    log("INFO", f"Creating backup: {backup_filename}", verbose)

    # Check if pg_dump is available
    if not subprocess.run(["which", "pg_dump"], capture_output=True).returncode == 0:
        # Try using kubectl exec into the postgres pod
        log("INFO", "pg_dump not found locally, using kubectl exec...", verbose)
        return create_backup_via_kubectl(params, backup_path, verbose)

    # Build pg_dump command
    env = os.environ.copy()
    env["PGPASSWORD"] = params["password"]

    cmd = [
        "pg_dump",
        "-h", params["host"],
        "-p", params["port"],
        "-U", params["user"],
        "-d", params["database"],
        "--format=plain",
        "--no-owner",
        "--no-acl"
    ]

    log("DEBUG", f"Running: {' '.join(cmd)}", verbose)

    try:
        # Run pg_dump and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            env=env,
            timeout=300  # 5 minute timeout
        )

        if result.returncode != 0:
            log("ERROR", f"pg_dump failed: {result.stderr.decode()}")
            return ""

        # Compress and write to file
        with gzip.open(backup_path, "wb") as f:
            f.write(result.stdout)

        file_size = backup_path.stat().st_size
        log("INFO", f"Backup created: {backup_path} ({file_size} bytes)", verbose)

        return str(backup_path)

    except subprocess.TimeoutExpired:
        log("ERROR", "pg_dump timed out")
        return ""
    except Exception as e:
        log("ERROR", f"Backup failed: {e}")
        return ""


def create_backup_via_kubectl(params: dict, backup_path: Path, verbose: bool = False) -> str:
    """Create backup by executing pg_dump inside the Kubernetes pod."""

    # Get pod name
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", NAMESPACE,
             "-l", "app.kubernetes.io/name=postgresql",
             "-o", "jsonpath={.items[0].metadata.name}"],
            capture_output=True, text=True, timeout=30
        )

        if result.returncode != 0 or not result.stdout.strip():
            log("ERROR", "Could not find PostgreSQL pod")
            return ""

        pod_name = result.stdout.strip()

    except Exception as e:
        log("ERROR", f"Could not get pod name: {e}")
        return ""

    log("INFO", f"Using pod: {pod_name}", verbose)

    # Execute pg_dump in pod
    cmd = [
        "kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
        "pg_dump",
        "-U", params["user"],
        "-d", params["database"],
        "--format=plain",
        "--no-owner",
        "--no-acl"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=300
        )

        if result.returncode != 0:
            log("ERROR", f"pg_dump in pod failed: {result.stderr.decode()}")
            return ""

        # Compress and write to file
        with gzip.open(backup_path, "wb") as f:
            f.write(result.stdout)

        file_size = backup_path.stat().st_size
        log("INFO", f"Backup created: {backup_path} ({file_size} bytes)", verbose)

        return str(backup_path)

    except subprocess.TimeoutExpired:
        log("ERROR", "pg_dump timed out")
        return ""
    except Exception as e:
        log("ERROR", f"Backup failed: {e}")
        return ""


def cleanup_old_backups(backup_dir: Path, keep_count: int = 10, verbose: bool = False):
    """Remove old backups, keeping only the most recent ones."""

    backups = sorted(backup_dir.glob("*.sql.gz"), key=lambda p: p.stat().st_mtime, reverse=True)

    if len(backups) > keep_count:
        for backup in backups[keep_count:]:
            log("INFO", f"Removing old backup: {backup.name}", verbose)
            backup.unlink()


def main():
    parser = argparse.ArgumentParser(description="Create PostgreSQL backup")
    parser.add_argument("--database", help="Database name (default: learnflow)")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_BACKUP_DIR,
                        help="Backup output directory")
    parser.add_argument("--keep", type=int, default=10,
                        help="Number of backups to keep (default: 10)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    log("INFO", "Starting backup", args.verbose)

    # Get connection parameters
    params = get_connection_params()

    if args.database:
        params["database"] = args.database

    if not params["password"]:
        log("ERROR", "No database password found")
        print("[ERROR] Database password not found")
        sys.exit(1)

    # Ensure backup directory exists
    if not ensure_backup_dir(args.output_dir):
        sys.exit(1)

    # Create backup
    backup_path = create_backup(params, args.output_dir, args.verbose)

    if backup_path:
        # Cleanup old backups
        cleanup_old_backups(args.output_dir, args.keep, args.verbose)

        print(f"[OK] Backup created: {backup_path}")
        sys.exit(0)
    else:
        print("[ERROR] Backup failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
