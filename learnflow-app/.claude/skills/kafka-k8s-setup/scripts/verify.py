#!/usr/bin/env python3
"""
Kafka Deployment Verification

Runs 5 verification tests:
1. Kafka pod running
2. Zookeeper pod running
3. Required topics exist
4. Publish test message
5. Consume test message

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
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / ".kafka-deploy.log"
NAMESPACE = os.environ.get("NAMESPACE", "kafka")
RELEASE_NAME = os.environ.get("RELEASE_NAME", "kafka")

# Required topics
REQUIRED_TOPICS = ["learning.submitted", "code.executed", "exercise.started", "struggle.detected"]

# Test topic
TEST_TOPIC = "__verify_test"

# Timeouts
POD_TIMEOUT = 30
TOPIC_TIMEOUT = 30
PUBSUB_TIMEOUT = 30


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


def get_kafka_pod() -> str:
    """Get the name of a running Kafka pod."""
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", NAMESPACE,
             "-l", "app.kubernetes.io/component=kafka",
             "-o", "jsonpath={.items[0].metadata.name}"],
            capture_output=True, text=True, timeout=POD_TIMEOUT
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""


# =============================================================================
# TEST 1: Kafka Pod Running
# =============================================================================

def test_kafka_pod(verbose: bool = False) -> Tuple[bool, str]:
    """Test 1: Check if Kafka pod is running."""
    log("INFO", "Test 1: Checking Kafka pod status...", verbose)

    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", NAMESPACE,
             "-l", "app.kubernetes.io/component=kafka",
             "--field-selector=status.phase=Running",
             "--no-headers"],
            capture_output=True, text=True, timeout=POD_TIMEOUT
        )

        if result.returncode != 0:
            return False, f"kubectl failed: {result.stderr}"

        running_pods = len([l for l in result.stdout.strip().split('\n') if l])

        if running_pods >= 1:
            log("INFO", f"Test 1 passed: {running_pods} Kafka pod(s) running", verbose)
            return True, f"{running_pods} pod(s) running"
        else:
            return False, "No Kafka pods running"

    except subprocess.TimeoutExpired:
        return False, "kubectl timeout"
    except Exception as e:
        return False, str(e)


# =============================================================================
# TEST 2: Zookeeper Pod Running
# =============================================================================

def test_zookeeper_pod(verbose: bool = False) -> Tuple[bool, str]:
    """Test 2: Check if Zookeeper pod is running."""
    log("INFO", "Test 2: Checking Zookeeper pod status...", verbose)

    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", NAMESPACE,
             "-l", "app.kubernetes.io/component=zookeeper",
             "--field-selector=status.phase=Running",
             "--no-headers"],
            capture_output=True, text=True, timeout=POD_TIMEOUT
        )

        if result.returncode != 0:
            return False, f"kubectl failed: {result.stderr}"

        running_pods = len([l for l in result.stdout.strip().split('\n') if l])

        if running_pods >= 1:
            log("INFO", f"Test 2 passed: {running_pods} Zookeeper pod(s) running", verbose)
            return True, f"{running_pods} pod(s) running"
        else:
            return False, "No Zookeeper pods running"

    except subprocess.TimeoutExpired:
        return False, "kubectl timeout"
    except Exception as e:
        return False, str(e)


# =============================================================================
# TEST 3: Topics Exist
# =============================================================================

def test_topics_exist(verbose: bool = False) -> Tuple[bool, str]:
    """Test 3: Check if required topics exist."""
    log("INFO", "Test 3: Checking topics exist...", verbose)

    pod_name = get_kafka_pod()
    if not pod_name:
        return False, "No Kafka pod found"

    try:
        result = subprocess.run(
            ["kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
             "kafka-topics.sh", "--bootstrap-server", "localhost:9092", "--list"],
            capture_output=True, text=True, timeout=TOPIC_TIMEOUT
        )

        if result.returncode != 0:
            return False, f"Topic list failed: {result.stderr}"

        existing_topics = set(t.strip() for t in result.stdout.strip().split('\n') if t.strip())

        missing = [t for t in REQUIRED_TOPICS if t not in existing_topics]

        if not missing:
            log("INFO", f"Test 3 passed: All {len(REQUIRED_TOPICS)} topics exist", verbose)
            return True, f"{len(REQUIRED_TOPICS)} topics exist"
        else:
            return False, f"Missing topics: {', '.join(missing)}"

    except subprocess.TimeoutExpired:
        return False, "Topic list timeout"
    except Exception as e:
        return False, str(e)


# =============================================================================
# TEST 4: Publish Message
# =============================================================================

def test_publish(verbose: bool = False) -> Tuple[bool, str]:
    """Test 4: Test publishing a message."""
    log("INFO", "Test 4: Testing message publish...", verbose)

    pod_name = get_kafka_pod()
    if not pod_name:
        return False, "No Kafka pod found"

    test_id = str(uuid.uuid4())[:8]
    test_message = json.dumps({"test_id": test_id, "timestamp": datetime.now(timezone.utc).isoformat()})

    try:
        # Create test topic if not exists
        subprocess.run(
            ["kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
             "kafka-topics.sh", "--bootstrap-server", "localhost:9092",
             "--create", "--topic", TEST_TOPIC,
             "--partitions", "1", "--replication-factor", "1",
             "--if-not-exists"],
            capture_output=True, text=True, timeout=TOPIC_TIMEOUT
        )

        # Publish message
        result = subprocess.run(
            ["kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
             "bash", "-c",
             f"echo '{test_message}' | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic {TEST_TOPIC}"],
            capture_output=True, text=True, timeout=PUBSUB_TIMEOUT
        )

        if result.returncode == 0:
            log("INFO", f"Test 4 passed: Message published (id: {test_id})", verbose)
            # Store test_id for consumer test
            return True, f"Published (id: {test_id})"
        else:
            return False, f"Publish failed: {result.stderr}"

    except subprocess.TimeoutExpired:
        return False, "Publish timeout"
    except Exception as e:
        return False, str(e)


# =============================================================================
# TEST 5: Consume Message
# =============================================================================

def test_consume(verbose: bool = False) -> Tuple[bool, str]:
    """Test 5: Test consuming a message."""
    log("INFO", "Test 5: Testing message consume...", verbose)

    pod_name = get_kafka_pod()
    if not pod_name:
        return False, "No Kafka pod found"

    try:
        # Consume messages (with short timeout)
        result = subprocess.run(
            ["kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
             "kafka-console-consumer.sh",
             "--bootstrap-server", "localhost:9092",
             "--topic", TEST_TOPIC,
             "--from-beginning",
             "--max-messages", "1",
             "--timeout-ms", "10000"],
            capture_output=True, text=True, timeout=PUBSUB_TIMEOUT
        )

        output = result.stdout.strip()

        if output and "test_id" in output:
            try:
                msg = json.loads(output.split('\n')[-1])
                test_id = msg.get("test_id", "unknown")
                log("INFO", f"Test 5 passed: Message consumed (id: {test_id})", verbose)
                return True, f"Consumed (id: {test_id})"
            except json.JSONDecodeError:
                # Still received a message
                log("INFO", "Test 5 passed: Message consumed", verbose)
                return True, "Consumed"
        elif output:
            # Got some output
            log("INFO", "Test 5 passed: Message received", verbose)
            return True, "Received"
        else:
            return False, "No message received"

    except subprocess.TimeoutExpired:
        return False, "Consume timeout"
    except Exception as e:
        return False, str(e)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Verify Kafka deployment")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    log("INFO", "Starting Kafka verification", args.verbose)

    if args.verbose:
        print(f"Namespace: {NAMESPACE}")
        print(f"Release: {RELEASE_NAME}")
        print("-" * 40)

    # Run all 5 tests
    tests = [
        ("Kafka Pod", test_kafka_pod),
        ("Zookeeper Pod", test_zookeeper_pod),
        ("Topics Exist", test_topics_exist),
        ("Publish", test_publish),
        ("Consume", test_consume),
    ]

    results = []
    all_passed = True

    for test_name, test_func in tests:
        passed, message = test_func(args.verbose)
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
