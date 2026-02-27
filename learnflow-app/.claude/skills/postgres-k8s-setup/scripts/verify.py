#!/usr/bin/env python3
"""
PostgreSQL Deployment Verification

Runs 5 verification tests:
1. Pod running check
2. Database connection test
3. Tables exist check
4. Data integrity test (INSERT/SELECT)
5. User privileges check

All 5 tests must pass for verification to succeed.

Usage:
    python verify.py
    python verify.py --verbose

Exit Codes:
    0 - All tests passed
    1 - One or more tests failed
"""

import argparse
import io
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / ".postgres-deploy.log"
CONNECTION_FILE = SCRIPT_DIR / ".connection"
NAMESPACE = os.environ.get("NAMESPACE", "postgres")
RELEASE_NAME = os.environ.get("RELEASE_NAME", "postgres")

# Test configuration
CONNECTION_TIMEOUT = 30  # seconds
CONNECTION_RETRIES = 5
RETRY_INTERVAL = 10  # seconds
QUERY_TIMEOUT = 10  # seconds

# Required tables
REQUIRED_TABLES = ["users", "classes", "quizzes", "submissions", "progress"]


def log(level: str, message: str, verbose: bool = False):
    """Log message to file and optionally stdout."""
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    log_line = f"[{timestamp}] [{level}] {message}"

    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")
    except Exception:
        pass

    if verbose or level == "ERROR":
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


# =============================================================================
# TEST 1: Pod Running Check
# =============================================================================

def test_pod_running(verbose: bool = False) -> Tuple[bool, str]:
    """
    Test 1: Check if PostgreSQL pod is running.

    Returns:
        Tuple[bool, str]: (passed, message)
    """
    log("INFO", "Test 1: Checking pod status...", verbose)

    try:
        # Get running pods
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", NAMESPACE,
             "-l", "app.kubernetes.io/name=postgresql",
             "--field-selector=status.phase=Running",
             "--no-headers"],
            capture_output=True, text=True, timeout=30
        )

        if result.returncode != 0:
            return False, f"kubectl failed: {result.stderr}"

        running_pods = len([line for line in result.stdout.strip().split('\n') if line])

        if running_pods >= 1:
            log("INFO", f"Test 1 passed: {running_pods} pod(s) running", verbose)
            return True, f"{running_pods} pod(s) running"
        else:
            return False, "No running pods found"

    except subprocess.TimeoutExpired:
        return False, "kubectl timeout"
    except Exception as e:
        return False, str(e)


# =============================================================================
# TEST 2: Database Connection Test
# =============================================================================

def test_connection(params: dict, verbose: bool = False) -> Tuple[bool, str]:
    """
    Test 2: Test database connection.

    Returns:
        Tuple[bool, str]: (passed, message)
    """
    log("INFO", "Test 2: Testing database connection...", verbose)

    try:
        import psycopg2
    except ImportError:
        return False, "psycopg2 not installed"

    for attempt in range(CONNECTION_RETRIES):
        try:
            conn = psycopg2.connect(
                host=params["host"],
                port=params["port"],
                user=params["user"],
                password=params["password"],
                database=params["database"],
                connect_timeout=CONNECTION_TIMEOUT
            )

            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            conn.close()

            if result and result[0] == 1:
                log("INFO", "Test 2 passed: Connection successful", verbose)
                return True, "Connection successful"
            else:
                return False, "SELECT 1 returned unexpected result"

        except psycopg2.OperationalError as e:
            log("DEBUG", f"Connection attempt {attempt + 1} failed: {e}", verbose)
            if attempt < CONNECTION_RETRIES - 1:
                time.sleep(RETRY_INTERVAL)
            else:
                return False, f"Connection failed after {CONNECTION_RETRIES} attempts: {e}"
        except Exception as e:
            return False, str(e)

    return False, "Connection test failed"


# =============================================================================
# TEST 3: Tables Exist Check
# =============================================================================

def test_tables_exist(params: dict, verbose: bool = False) -> Tuple[bool, str]:
    """
    Test 3: Check if required tables exist.

    Returns:
        Tuple[bool, str]: (passed, message)
    """
    log("INFO", "Test 3: Checking tables exist...", verbose)

    try:
        import psycopg2

        conn = psycopg2.connect(
            host=params["host"],
            port=params["port"],
            user=params["user"],
            password=params["password"],
            database=params["database"],
            connect_timeout=CONNECTION_TIMEOUT
        )

        cursor = conn.cursor()

        # Get all tables in public schema
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        """)

        existing_tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        missing_tables = [t for t in REQUIRED_TABLES if t not in existing_tables]

        if not missing_tables:
            log("INFO", f"Test 3 passed: {len(REQUIRED_TABLES)} required tables exist", verbose)
            return True, f"{len(REQUIRED_TABLES)} tables exist"
        else:
            return False, f"Missing tables: {', '.join(missing_tables)}"

    except Exception as e:
        return False, str(e)


# =============================================================================
# TEST 4: Data Integrity Test
# =============================================================================

def test_data_integrity(params: dict, verbose: bool = False) -> Tuple[bool, str]:
    """
    Test 4: Test INSERT/SELECT operations.

    Returns:
        Tuple[bool, str]: (passed, message)
    """
    log("INFO", "Test 4: Testing data integrity...", verbose)

    try:
        import psycopg2

        conn = psycopg2.connect(
            host=params["host"],
            port=params["port"],
            user=params["user"],
            password=params["password"],
            database=params["database"],
            connect_timeout=CONNECTION_TIMEOUT
        )
        conn.autocommit = False

        cursor = conn.cursor()
        test_email = f"test_{int(time.time())}@verify.test"

        try:
            # Insert test user
            cursor.execute("""
                INSERT INTO users (email, username, password_hash, role)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (test_email, f"test_user_{int(time.time())}", "test_hash", "student"))

            user_id = cursor.fetchone()[0]

            # Select it back
            cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()

            if result and result[0] == test_email:
                # Rollback to clean up test data
                conn.rollback()
                log("INFO", "Test 4 passed: INSERT/SELECT successful", verbose)
                return True, "INSERT/SELECT successful"
            else:
                conn.rollback()
                return False, "SELECT returned wrong data"

        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()

    except Exception as e:
        return False, str(e)


# =============================================================================
# TEST 5: User Privileges Check
# =============================================================================

def test_privileges(params: dict, verbose: bool = False) -> Tuple[bool, str]:
    """
    Test 5: Check database user privileges.

    Returns:
        Tuple[bool, str]: (passed, message)
    """
    log("INFO", "Test 5: Checking user privileges...", verbose)

    try:
        import psycopg2

        conn = psycopg2.connect(
            host=params["host"],
            port=params["port"],
            user=params["user"],
            password=params["password"],
            database=params["database"],
            connect_timeout=CONNECTION_TIMEOUT
        )

        cursor = conn.cursor()

        # Check current user's roles
        cursor.execute("""
            SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin
            FROM pg_roles
            WHERE rolname = current_user
        """)

        result = cursor.fetchone()
        conn.close()

        if result:
            rolname, is_super, can_create_role, can_create_db, can_login = result

            if can_login:
                privileges = []
                if is_super:
                    privileges.append("superuser")
                if can_create_role:
                    privileges.append("createrole")
                if can_create_db:
                    privileges.append("createdb")

                log("INFO", f"Test 5 passed: User '{rolname}' has login privilege", verbose)
                return True, f"User '{rolname}' can login"
            else:
                return False, f"User '{rolname}' cannot login"
        else:
            return False, "Could not get user role info"

    except Exception as e:
        return False, str(e)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Verify PostgreSQL deployment")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    log("INFO", "Starting PostgreSQL verification", args.verbose)

    # Get connection parameters
    params = get_connection_params()

    if args.verbose:
        print(f"Host: {params['host']}")
        print(f"Port: {params['port']}")
        print(f"Database: {params['database']}")
        print("-" * 40)

    # Run all 5 tests
    tests = [
        ("Pod Running", lambda: test_pod_running(args.verbose)),
        ("Connection", lambda: test_connection(params, args.verbose)),
        ("Tables Exist", lambda: test_tables_exist(params, args.verbose)),
        ("Data Integrity", lambda: test_data_integrity(params, args.verbose)),
        ("User Privileges", lambda: test_privileges(params, args.verbose)),
    ]

    results = []
    all_passed = True

    for test_name, test_func in tests:
        passed, message = test_func()
        results.append((test_name, passed, message))

        if args.verbose:
            status = "[OK]" if passed else "[FAIL]"
            print(f"  {status} {test_name}: {message}")

        if not passed:
            all_passed = False

    if args.verbose:
        print("-" * 40)

    # Summary
    passed_count = sum(1 for _, p, _ in results if p)

    if all_passed:
        log("INFO", "All 5 tests passed", args.verbose)
        print(f"[OK] All 5 tests passed")
        sys.exit(0)
    else:
        failed = [(name, msg) for name, passed, msg in results if not passed]
        log("ERROR", f"{len(failed)} test(s) failed", args.verbose)
        print(f"[ERROR] {passed_count}/5 tests passed")
        for name, msg in failed:
            print(f"  - {name}: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
