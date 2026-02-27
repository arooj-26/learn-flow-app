#!/usr/bin/env python3
"""
Kafka Topic Creation Script

Creates required topics with specific configurations:
- learning.submitted (3 partitions, 7 day retention)
- code.executed (3 partitions, 7 day retention)
- exercise.started (3 partitions, 7 day retention)
- struggle.detected (3 partitions, 3 day retention)

Usage:
    python create_topics.py
    python create_topics.py --dry-run
    python create_topics.py --list-only

Exit Codes:
    0 - Success
    1 - Failure
"""

import argparse
import io
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / ".kafka-deploy.log"
CONNECTION_FILE = SCRIPT_DIR / ".connection"
NAMESPACE = os.environ.get("NAMESPACE", "kafka")
RELEASE_NAME = os.environ.get("RELEASE_NAME", "kafka")

# Topic specifications
TOPICS = {
    "learning.submitted": {
        "partitions": 3,
        "replication_factor": 1,
        "retention_ms": 7 * 24 * 60 * 60 * 1000,  # 7 days
        "description": "Student assignment and quiz submissions"
    },
    "code.executed": {
        "partitions": 3,
        "replication_factor": 1,
        "retention_ms": 7 * 24 * 60 * 60 * 1000,  # 7 days
        "description": "Code execution events for analytics"
    },
    "exercise.started": {
        "partitions": 3,
        "replication_factor": 1,
        "retention_ms": 7 * 24 * 60 * 60 * 1000,  # 7 days
        "description": "Exercise start events"
    },
    "struggle.detected": {
        "partitions": 3,
        "replication_factor": 1,
        "retention_ms": 3 * 24 * 60 * 60 * 1000,  # 3 days
        "description": "AI-detected learning struggles"
    }
}

# Retry configuration
MAX_RETRIES = 3
RETRY_INTERVAL = 5  # seconds
TOPIC_TIMEOUT = 30  # seconds


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


def get_kafka_pod() -> Optional[str]:
    """Get the name of a running Kafka pod."""
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", NAMESPACE,
             "-l", "app.kubernetes.io/component=kafka",
             "-o", "jsonpath={.items[0].metadata.name}"],
            capture_output=True, text=True, timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

    except Exception as e:
        log("ERROR", f"Failed to get Kafka pod: {e}")

    return None


def get_bootstrap_servers() -> str:
    """Get Kafka bootstrap servers address."""
    # Try connection file first
    if CONNECTION_FILE.exists():
        try:
            with open(CONNECTION_FILE) as f:
                for line in f:
                    if line.startswith("KAFKA_BOOTSTRAP_SERVERS="):
                        return line.strip().split("=", 1)[1]
        except Exception:
            pass

    # Default
    return f"{RELEASE_NAME}-headless.{NAMESPACE}.svc.cluster.local:9092"


def list_existing_topics(pod_name: str, verbose: bool = False) -> List[str]:
    """List existing Kafka topics."""
    try:
        result = subprocess.run(
            ["kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
             "kafka-topics.sh", "--bootstrap-server", "localhost:9092", "--list"],
            capture_output=True, text=True, timeout=TOPIC_TIMEOUT
        )

        if result.returncode == 0:
            topics = [t.strip() for t in result.stdout.strip().split('\n') if t.strip()]
            log("DEBUG", f"Existing topics: {topics}", verbose)
            return topics
        else:
            log("ERROR", f"Failed to list topics: {result.stderr}")

    except subprocess.TimeoutExpired:
        log("ERROR", "Timeout listing topics")
    except Exception as e:
        log("ERROR", f"Failed to list topics: {e}")

    return []


def create_topic(pod_name: str, topic_name: str, config: dict,
                 verbose: bool = False) -> Tuple[bool, str]:
    """
    Create a single Kafka topic.

    Returns:
        Tuple[bool, str]: (success, message)
    """
    partitions = config["partitions"]
    replication_factor = config["replication_factor"]
    retention_ms = config["retention_ms"]

    for attempt in range(MAX_RETRIES):
        try:
            cmd = [
                "kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
                "kafka-topics.sh",
                "--bootstrap-server", "localhost:9092",
                "--create",
                "--topic", topic_name,
                "--partitions", str(partitions),
                "--replication-factor", str(replication_factor),
                "--config", f"retention.ms={retention_ms}",
                "--if-not-exists"
            ]

            log("DEBUG", f"Creating topic: {' '.join(cmd)}", verbose)

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=TOPIC_TIMEOUT
            )

            if result.returncode == 0:
                log("INFO", f"Created topic: {topic_name}", verbose)
                return True, "created"
            elif "already exists" in result.stderr.lower():
                log("INFO", f"Topic already exists: {topic_name}", verbose)
                return True, "exists"
            else:
                log("WARN", f"Attempt {attempt + 1} failed: {result.stderr}", verbose)

        except subprocess.TimeoutExpired:
            log("WARN", f"Timeout creating topic (attempt {attempt + 1})", verbose)
        except Exception as e:
            log("WARN", f"Error creating topic (attempt {attempt + 1}): {e}", verbose)

        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_INTERVAL)

    return False, "failed after retries"


def main():
    parser = argparse.ArgumentParser(description="Create Kafka topics")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    parser.add_argument("--list-only", action="store_true", help="Only list existing topics")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    log("INFO", "Starting topic creation", args.verbose)

    # Get Kafka pod
    pod_name = get_kafka_pod()
    if not pod_name:
        print("[ERROR] No Kafka pod found")
        sys.exit(1)

    log("INFO", f"Using Kafka pod: {pod_name}", args.verbose)

    # List existing topics
    existing = list_existing_topics(pod_name, args.verbose)

    if args.list_only:
        print(f"[INFO] {len(existing)} existing topic(s):")
        for topic in existing:
            print(f"  - {topic}")
        sys.exit(0)

    # Dry run
    if args.dry_run:
        print(f"[DRY RUN] Would create {len(TOPICS)} topic(s):")
        for topic_name, config in TOPICS.items():
            status = "exists" if topic_name in existing else "create"
            print(f"  - {topic_name} ({status})")
            print(f"    Partitions: {config['partitions']}")
            print(f"    Retention: {config['retention_ms'] // (24*60*60*1000)} days")
        sys.exit(0)

    # Create topics
    created = 0
    skipped = 0
    failed = 0

    for topic_name, config in TOPICS.items():
        if topic_name in existing:
            log("INFO", f"Topic already exists: {topic_name}", args.verbose)
            skipped += 1
            continue

        success, status = create_topic(pod_name, topic_name, config, args.verbose)

        if success:
            if status == "exists":
                skipped += 1
            else:
                created += 1
        else:
            failed += 1

    # Summary
    total = len(TOPICS)

    if failed > 0:
        print(f"[ERROR] {failed}/{total} topic(s) failed")
        sys.exit(1)
    elif created > 0:
        print(f"[OK] {created} topic(s) created, {skipped} already existed")
    else:
        print(f"[OK] All {total} topic(s) already exist")

    sys.exit(0)


if __name__ == "__main__":
    main()
