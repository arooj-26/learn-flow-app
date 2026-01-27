#!/usr/bin/env python3
"""
Test a deployed FastAPI + Dapr microservice.

Runs 5 tests:
  1. Pod running in Kubernetes
  2. /health endpoint responds HTTP 200
  3. Dapr sidecar running
  4. Can publish to Kafka topic
  5. State management save/retrieve works

Usage:
    python test_service.py <service-name> [namespace]
    python test_service.py triage-agent
    python test_service.py triage-agent production
"""

import json
import subprocess
import sys
import time

SERVICE_NAME = sys.argv[1] if len(sys.argv) > 1 else None
NAMESPACE = sys.argv[2] if len(sys.argv) > 2 else "default"

if not SERVICE_NAME:
    print("ERROR: Service name required. Usage: python test_service.py <service-name> [namespace]")
    sys.exit(1)


class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.message = ""
        self.duration_ms = 0

    def __str__(self):
        status = "PASS" if self.passed else "FAIL"
        return f"  [{status}] {self.name}: {self.message} ({self.duration_ms}ms)"


def run_kubectl(args: list, timeout: int = 30) -> tuple:
    """Run a kubectl command and return (returncode, stdout, stderr)."""
    cmd = ["kubectl"] + args + ["-n", NAMESPACE]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except FileNotFoundError:
        return 1, "", "kubectl not found"


def get_pod_name() -> str:
    """Get the pod name for the service."""
    rc, stdout, _ = run_kubectl([
        "get", "pods", "-l", f"app={SERVICE_NAME}",
        "-o", "jsonpath={.items[0].metadata.name}"
    ])
    return stdout if rc == 0 else ""


def test_pod_running() -> TestResult:
    """Test 1: Service pod is running."""
    result = TestResult("Pod running")
    start = time.time()

    rc, stdout, stderr = run_kubectl([
        "get", "pods", "-l", f"app={SERVICE_NAME}",
        "-o", "jsonpath={.items[0].status.phase}"
    ])

    result.duration_ms = int((time.time() - start) * 1000)

    if rc != 0:
        result.message = f"kubectl failed: {stderr}"
        return result

    if stdout == "Running":
        result.passed = True
        result.message = f"Pod is in Running phase"
    else:
        result.message = f"Pod phase: {stdout or 'not found'}"

    return result


def test_health_endpoint() -> TestResult:
    """Test 2: /health endpoint responds with HTTP 200."""
    result = TestResult("/health endpoint")
    start = time.time()

    pod_name = get_pod_name()
    if not pod_name:
        result.message = "No pod found"
        result.duration_ms = int((time.time() - start) * 1000)
        return result

    # Port-forward and test health
    rc, stdout, stderr = run_kubectl([
        "exec", pod_name, "--",
        "python", "-c",
        "import urllib.request; "
        "r = urllib.request.urlopen('http://localhost:8000/health'); "
        "print(r.status, r.read().decode())"
    ])

    result.duration_ms = int((time.time() - start) * 1000)

    if rc == 0 and "200" in stdout:
        try:
            # Parse the response body (after "200 ")
            body = stdout.split(" ", 1)[1] if " " in stdout else stdout
            data = json.loads(body)
            if data.get("status") == "healthy":
                result.passed = True
                result.message = "Healthy"
            else:
                result.message = f"Unexpected status: {data.get('status')}"
        except (json.JSONDecodeError, IndexError):
            if "healthy" in stdout.lower():
                result.passed = True
                result.message = "Healthy (raw)"
            else:
                result.message = f"Unexpected response: {stdout[:100]}"
    else:
        result.message = f"Health check failed: {stderr or stdout}"

    return result


def test_dapr_sidecar() -> TestResult:
    """Test 3: Dapr sidecar is running."""
    result = TestResult("Dapr sidecar running")
    start = time.time()

    pod_name = get_pod_name()
    if not pod_name:
        result.message = "No pod found"
        result.duration_ms = int((time.time() - start) * 1000)
        return result

    rc, stdout, stderr = run_kubectl([
        "get", "pod", pod_name,
        "-o", "jsonpath={.status.containerStatuses[?(@.name==\"daprd\")].ready}"
    ])

    result.duration_ms = int((time.time() - start) * 1000)

    if rc == 0 and stdout == "true":
        result.passed = True
        result.message = "Sidecar is ready"
    else:
        result.message = f"Sidecar not ready: {stdout or stderr}"

    return result


def test_kafka_publish() -> TestResult:
    """Test 4: Can publish to Kafka topic via Dapr."""
    result = TestResult("Kafka publish")
    start = time.time()

    pod_name = get_pod_name()
    if not pod_name:
        result.message = "No pod found"
        result.duration_ms = int((time.time() - start) * 1000)
        return result

    test_data = json.dumps({"test": True, "timestamp": time.time()})

    rc, stdout, stderr = run_kubectl([
        "exec", pod_name, "--",
        "python", "-c",
        f"from dapr.clients import DaprClient; "
        f"c = DaprClient(); "
        f"c.publish_event('kafka', 'learning.test', '{test_data}', "
        f"data_content_type='application/json'); "
        f"print('published')"
    ])

    result.duration_ms = int((time.time() - start) * 1000)

    if rc == 0 and "published" in stdout:
        result.passed = True
        result.message = "Published test event to learning.test"
    else:
        result.message = f"Publish failed: {stderr or stdout}"

    return result


def test_state_management() -> TestResult:
    """Test 5: State management save/retrieve works."""
    result = TestResult("State management")
    start = time.time()

    pod_name = get_pod_name()
    if not pod_name:
        result.message = "No pod found"
        result.duration_ms = int((time.time() - start) * 1000)
        return result

    test_key = f"test-{SERVICE_NAME}-{int(time.time())}"
    test_value = json.dumps({"test": True, "service": SERVICE_NAME})

    # Save and retrieve state
    rc, stdout, stderr = run_kubectl([
        "exec", pod_name, "--",
        "python", "-c",
        f"import json; "
        f"from dapr.clients import DaprClient; "
        f"c = DaprClient(); "
        f"c.save_state('postgres', '{test_key}', '{test_value}'); "
        f"r = c.get_state('postgres', '{test_key}'); "
        f"d = json.loads(r.data) if r.data else None; "
        f"c.delete_state('postgres', '{test_key}'); "
        f"print('ok' if d and d.get('test') else 'fail')"
    ])

    result.duration_ms = int((time.time() - start) * 1000)

    if rc == 0 and "ok" in stdout:
        result.passed = True
        result.message = "Save/retrieve/delete cycle successful"
    else:
        result.message = f"State test failed: {stderr or stdout}"

    return result


def main():
    print(f"Testing service: {SERVICE_NAME} (namespace: {NAMESPACE})")
    print("-" * 60)

    tests = [
        test_pod_running,
        test_health_endpoint,
        test_dapr_sidecar,
        test_kafka_publish,
        test_state_management,
    ]

    results = []
    for test_fn in tests:
        result = test_fn()
        results.append(result)
        print(result)

    print("-" * 60)

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    total_ms = sum(r.duration_ms for r in results)

    print(f"Results: {passed}/{total} passed ({total_ms}ms total)")

    if passed == total:
        print(f"Service {SERVICE_NAME} is fully operational")
        sys.exit(0)
    else:
        failed = [r.name for r in results if not r.passed]
        print(f"FAILED: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
