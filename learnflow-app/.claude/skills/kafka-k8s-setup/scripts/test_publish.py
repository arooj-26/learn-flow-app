#!/usr/bin/env python3
"""
Kafka Pub/Sub Test Script

Tests publish and consume functionality:
1. Create producer
2. Publish JSON message with timestamp
3. Create consumer
4. Consume and verify message

Usage:
    python test_publish.py
    python test_publish.py --topic learning.submitted
    python test_publish.py --verbose

Exit Codes:
    0 - Success (pub/sub working)
    1 - Failure
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
from typing import Optional, Tuple

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / ".kafka-deploy.log"
NAMESPACE = os.environ.get("NAMESPACE", "kafka")
RELEASE_NAME = os.environ.get("RELEASE_NAME", "kafka")

# Default test topic
DEFAULT_TOPIC = "__pubsub_test"

# Timeouts
PUBLISH_TIMEOUT = 30
CONSUME_TIMEOUT = 30


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
    except Exception:
        pass
    return None


def ensure_topic(pod_name: str, topic: str, verbose: bool = False) -> bool:
    """Ensure test topic exists."""
    try:
        result = subprocess.run(
            ["kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
             "kafka-topics.sh", "--bootstrap-server", "localhost:9092",
             "--create", "--topic", topic,
             "--partitions", "1", "--replication-factor", "1",
             "--if-not-exists"],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0 or "already exists" in result.stderr.lower()
    except Exception as e:
        log("ERROR", f"Failed to create topic: {e}", verbose)
        return False


def publish_message(pod_name: str, topic: str, message: dict,
                   verbose: bool = False) -> Tuple[bool, str]:
    """
    Publish a message to Kafka topic.

    Returns:
        Tuple[bool, str]: (success, error_message)
    """
    try:
        message_json = json.dumps(message)
        log("DEBUG", f"Publishing to {topic}: {message_json}", verbose)

        result = subprocess.run(
            ["kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
             "bash", "-c",
             f"echo '{message_json}' | kafka-console-producer.sh --bootstrap-server localhost:9092 --topic {topic}"],
            capture_output=True, text=True, timeout=PUBLISH_TIMEOUT
        )

        if result.returncode == 0:
            log("INFO", f"Published message to {topic}", verbose)
            return True, ""
        else:
            return False, result.stderr

    except subprocess.TimeoutExpired:
        return False, "Publish timeout"
    except Exception as e:
        return False, str(e)


def consume_message(pod_name: str, topic: str, expected_id: str,
                   verbose: bool = False) -> Tuple[bool, Optional[dict]]:
    """
    Consume and verify a message from Kafka topic.

    Returns:
        Tuple[bool, Optional[dict]]: (success, message_data)
    """
    try:
        # Use a unique consumer group for this test
        group_id = f"test-{uuid.uuid4().hex[:8]}"

        result = subprocess.run(
            ["kubectl", "exec", "-n", NAMESPACE, pod_name, "--",
             "kafka-console-consumer.sh",
             "--bootstrap-server", "localhost:9092",
             "--topic", topic,
             "--from-beginning",
             "--max-messages", "10",
             "--timeout-ms", "15000",
             "--group", group_id],
            capture_output=True, text=True, timeout=CONSUME_TIMEOUT
        )

        output = result.stdout.strip()
        log("DEBUG", f"Consumer output: {output}", verbose)

        if not output:
            return False, None

        # Parse messages and find our test message
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue

            try:
                msg = json.loads(line)
                if msg.get("test_id") == expected_id:
                    log("INFO", f"Found test message: {expected_id}", verbose)
                    return True, msg
            except json.JSONDecodeError:
                continue

        # Check if we got any message at all
        log("WARN", f"Test message {expected_id} not found in output", verbose)
        return False, None

    except subprocess.TimeoutExpired:
        return False, None
    except Exception as e:
        log("ERROR", f"Consume failed: {e}", verbose)
        return False, None


def run_pubsub_test(topic: str, verbose: bool = False) -> Tuple[bool, str]:
    """
    Run full pub/sub test.

    Returns:
        Tuple[bool, str]: (success, message)
    """
    # Get Kafka pod
    pod_name = get_kafka_pod()
    if not pod_name:
        return False, "No Kafka pod found"

    log("INFO", f"Using Kafka pod: {pod_name}", verbose)

    # Ensure topic exists
    if not ensure_topic(pod_name, topic, verbose):
        return False, f"Failed to ensure topic: {topic}"

    # Generate test message
    test_id = uuid.uuid4().hex[:8]
    test_message = {
        "test_id": test_id,
        "event_type": "pubsub_test",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": {
            "source": "test_publish.py",
            "topic": topic
        }
    }

    # Publish message
    log("INFO", f"Publishing test message (id: {test_id})", verbose)
    success, error = publish_message(pod_name, topic, test_message, verbose)

    if not success:
        return False, f"Publish failed: {error}"

    # Small delay to allow message propagation
    time.sleep(1)

    # Consume and verify
    log("INFO", "Consuming messages...", verbose)
    success, received = consume_message(pod_name, topic, test_id, verbose)

    if success and received:
        return True, f"test_id: {test_id}"
    else:
        return False, "Message not received"


def main():
    parser = argparse.ArgumentParser(description="Test Kafka pub/sub")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help=f"Topic to test (default: {DEFAULT_TOPIC})")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    log("INFO", f"Starting pub/sub test on topic: {args.topic}", args.verbose)

    if args.verbose:
        print(f"Topic: {args.topic}")
        print(f"Namespace: {NAMESPACE}")
        print("-" * 40)

    success, message = run_pubsub_test(args.topic, args.verbose)

    if args.verbose:
        print("-" * 40)

    if success:
        print(f"[OK] Pub/Sub working ({message})")
        sys.exit(0)
    else:
        print(f"[ERROR] Pub/Sub failed: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
