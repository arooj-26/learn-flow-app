#!/usr/bin/env python3
"""
Verify Next.js Kubernetes Deployment

Validates that the Next.js application is correctly deployed and healthy:
- Pod status and readiness
- Service endpoint connectivity
- Health check endpoint response
- API backend connectivity (optional)
- Resource utilization checks

Usage:
    python verify.py --namespace frontend --release frontend-app
    python verify.py --namespace frontend --release frontend-app --port 30080
    python verify.py --namespace frontend --release frontend-app --api-url http://api-svc:8000/health
    python verify.py --verbose

Exit Codes:
    0 - All checks passed
    1 - Fatal verification failure
    2 - Prerequisites not met
    4 - Health check timeout
"""

import argparse
import io
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Windows UTF-8 compatibility
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ─── Configuration ────────────────────────────────────────────────────────────

DEBUG = os.environ.get("DEBUG", "0") == "1"
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = os.environ.get("LOG_FILE", str(SCRIPT_DIR.parent / ".nextjs-k8s-deploy.log"))


# ─── Logging ──────────────────────────────────────────────────────────────────

def log(level: str, message: str, verbose: bool = False):
    """Log to file and optionally stdout."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    log_line = f"[{timestamp}] [{level}] {message}"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except OSError:
        pass

    if DEBUG or verbose or level == "ERROR":
        if level == "ERROR":
            print(log_line, file=sys.stderr)
        else:
            print(log_line)


# ─── Kubectl Helpers ──────────────────────────────────────────────────────────

def run_kubectl(args: list[str], timeout: int = 30) -> tuple[bool, str]:
    """Run kubectl command and return (success, output)."""
    cmd = ["kubectl"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, output
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, "kubectl not found"


def get_json(args: list[str]) -> tuple[bool, dict]:
    """Run kubectl with JSON output."""
    success, output = run_kubectl(args + ["-o", "json"])
    if not success:
        return False, {}
    try:
        return True, json.loads(output)
    except json.JSONDecodeError:
        return False, {}


# ─── Verification Checks ─────────────────────────────────────────────────────

class VerificationResult:
    def __init__(self):
        self.checks: list[dict] = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def add(self, name: str, status: str, message: str):
        self.checks.append({"name": name, "status": status, "message": message})
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        elif status == "WARN":
            self.warnings += 1

    @property
    def success(self) -> bool:
        return self.failed == 0


def check_prerequisites(verbose: bool) -> bool:
    """Verify kubectl is available and cluster is accessible."""
    log("INFO", "Checking prerequisites...", verbose)

    success, output = run_kubectl(["cluster-info"])
    if not success:
        log("ERROR", f"Kubernetes cluster not accessible: {output}")
        return False

    log("INFO", "Kubernetes cluster accessible", verbose)
    return True


def check_namespace(namespace: str, verbose: bool, result: VerificationResult):
    """Verify namespace exists."""
    log("INFO", f"Checking namespace: {namespace}", verbose)

    success, _ = run_kubectl(["get", "namespace", namespace])
    if success:
        result.add("Namespace", "PASS", f"Namespace '{namespace}' exists")
    else:
        result.add("Namespace", "FAIL", f"Namespace '{namespace}' not found")


def check_deployment(namespace: str, release: str, verbose: bool, result: VerificationResult):
    """Verify deployment exists and is healthy."""
    log("INFO", f"Checking deployment: {release}", verbose)

    success, data = get_json(["get", "deployment", release, "-n", namespace])
    if not success:
        result.add("Deployment", "FAIL", f"Deployment '{release}' not found in namespace '{namespace}'")
        return

    spec = data.get("spec", {})
    status = data.get("status", {})

    desired = spec.get("replicas", 0)
    ready = status.get("readyReplicas", 0)
    available = status.get("availableReplicas", 0)
    updated = status.get("updatedReplicas", 0)

    if ready == desired and available == desired:
        result.add("Deployment", "PASS", f"{ready}/{desired} replicas ready")
    elif ready > 0:
        result.add("Deployment", "WARN", f"{ready}/{desired} replicas ready ({available} available)")
    else:
        result.add("Deployment", "FAIL", f"0/{desired} replicas ready")

    # Check image
    containers = spec.get("template", {}).get("spec", {}).get("containers", [])
    if containers:
        image = containers[0].get("image", "unknown")
        result.add("Image", "PASS", f"Image: {image}")
        log("INFO", f"Container image: {image}", verbose)


def check_pods(namespace: str, release: str, verbose: bool, result: VerificationResult):
    """Verify pod status."""
    log("INFO", "Checking pods...", verbose)

    success, data = get_json(["get", "pods", "-n", namespace, "-l", f"app={release}"])
    if not success:
        result.add("Pods", "FAIL", "Could not list pods")
        return

    pods = data.get("items", [])
    if not pods:
        result.add("Pods", "FAIL", "No pods found")
        return

    running = 0
    issues = []

    for pod in pods:
        pod_name = pod.get("metadata", {}).get("name", "unknown")
        phase = pod.get("status", {}).get("phase", "Unknown")

        if phase == "Running":
            running += 1
        else:
            issues.append(f"{pod_name}: {phase}")

        # Check container statuses
        container_statuses = pod.get("status", {}).get("containerStatuses", [])
        for cs in container_statuses:
            if not cs.get("ready", False):
                waiting = cs.get("state", {}).get("waiting", {})
                reason = waiting.get("reason", "Unknown")
                if reason != "Unknown":
                    issues.append(f"{pod_name}: {reason}")

        # Check restart count
        for cs in container_statuses:
            restarts = cs.get("restartCount", 0)
            if restarts > 3:
                issues.append(f"{pod_name}: {restarts} restarts")

    if issues:
        result.add("Pods", "WARN", f"{running} running, issues: {'; '.join(issues)}")
    elif running > 0:
        result.add("Pods", "PASS", f"{running}/{len(pods)} pods running")
    else:
        result.add("Pods", "FAIL", "No running pods")


def check_service(namespace: str, release: str, expected_port: int, verbose: bool, result: VerificationResult):
    """Verify service exists and has correct port."""
    log("INFO", f"Checking service: {release}-svc", verbose)

    svc_name = f"{release}-svc"
    success, data = get_json(["get", "service", svc_name, "-n", namespace])
    if not success:
        result.add("Service", "FAIL", f"Service '{svc_name}' not found")
        return

    spec = data.get("spec", {})
    svc_type = spec.get("type", "Unknown")
    ports = spec.get("ports", [])

    if not ports:
        result.add("Service", "FAIL", "No ports configured")
        return

    port_info = ports[0]
    node_port = port_info.get("nodePort", 0)
    target_port = port_info.get("targetPort", 0)

    if node_port == expected_port:
        result.add("Service", "PASS", f"{svc_type} port {node_port} -> {target_port}")
    elif node_port > 0:
        result.add("Service", "WARN", f"NodePort is {node_port}, expected {expected_port}")
    else:
        result.add("Service", "FAIL", f"NodePort not assigned")


def check_health_endpoint(namespace: str, release: str, port: int, timeout: int, verbose: bool, result: VerificationResult):
    """Verify health check endpoint responds correctly."""
    log("INFO", "Checking health endpoint...", verbose)

    # Try via kubectl exec into a pod
    success, pods_output = run_kubectl([
        "get", "pods", "-n", namespace,
        "-l", f"app={release}",
        "--field-selector=status.phase=Running",
        "-o", "jsonpath={.items[0].metadata.name}",
    ])

    if not success or not pods_output:
        result.add("Health Check", "FAIL", "No running pod found for health check")
        return

    pod_name = pods_output.strip()
    container_port = 3000  # Default Next.js port

    max_attempts = 5
    delay = 5

    for attempt in range(1, max_attempts + 1):
        success, health_output = run_kubectl([
            "exec", "-n", namespace, pod_name, "--",
            "wget", "-q", "-O", "-", f"http://localhost:{container_port}/api/health",
        ], timeout=15)

        if success:
            try:
                health_data = json.loads(health_output)
                status = health_data.get("status", "unknown")
                if status == "healthy":
                    result.add("Health Check", "PASS", f"Endpoint healthy (pod: {pod_name})")
                    return
                else:
                    result.add("Health Check", "WARN", f"Status: {status}")
                    return
            except json.JSONDecodeError:
                log("DEBUG", f"Health response not JSON: {health_output[:100]}", verbose)

        if attempt < max_attempts:
            log("DEBUG", f"Health check attempt {attempt} failed, retrying...", verbose)
            time.sleep(delay)

    result.add("Health Check", "FAIL", f"Health endpoint not responding after {max_attempts} attempts")


def check_api_connectivity(namespace: str, release: str, api_url: str, verbose: bool, result: VerificationResult):
    """Verify API backend is reachable from pods."""
    if not api_url:
        log("DEBUG", "No API URL provided, skipping connectivity check", verbose)
        return

    log("INFO", f"Checking API connectivity: {api_url}", verbose)

    success, pods_output = run_kubectl([
        "get", "pods", "-n", namespace,
        "-l", f"app={release}",
        "--field-selector=status.phase=Running",
        "-o", "jsonpath={.items[0].metadata.name}",
    ])

    if not success or not pods_output:
        result.add("API Connectivity", "WARN", "No running pod for connectivity check")
        return

    pod_name = pods_output.strip()
    success, output = run_kubectl([
        "exec", "-n", namespace, pod_name, "--",
        "wget", "-q", "-O", "-", "--timeout=10", api_url,
    ], timeout=15)

    if success:
        result.add("API Connectivity", "PASS", f"Backend reachable: {api_url}")
    else:
        result.add("API Connectivity", "WARN", f"Backend not reachable: {api_url} ({output[:80]})")


def check_resource_usage(namespace: str, release: str, verbose: bool, result: VerificationResult):
    """Check resource utilization of pods."""
    log("INFO", "Checking resource usage...", verbose)

    success, output = run_kubectl([
        "top", "pods", "-n", namespace, "-l", f"app={release}",
    ])

    if not success:
        log("DEBUG", "kubectl top not available (metrics-server may not be installed)", verbose)
        result.add("Resources", "WARN", "Metrics not available (metrics-server may not be installed)")
        return

    result.add("Resources", "PASS", "Resource metrics available")
    log("INFO", f"Resource usage:\n{output}", verbose)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Verify Next.js Kubernetes deployment")
    parser.add_argument("--namespace", default="frontend", help="Kubernetes namespace")
    parser.add_argument("--release", default="frontend-app", help="Deployment/release name")
    parser.add_argument("--port", type=int, default=30080, help="NodePort to verify")
    parser.add_argument("--api-url", default="", help="Backend API URL to verify connectivity")
    parser.add_argument("--timeout", type=int, default=120, help="Verification timeout (seconds)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    verbose = args.verbose or DEBUG
    log("INFO", "=== Deployment Verification ===", verbose)
    log("INFO", f"Namespace: {args.namespace} | Release: {args.release} | Port: {args.port}", verbose)

    # Prerequisites
    if not check_prerequisites(verbose):
        print("[ERROR] Prerequisites not met", file=sys.stderr)
        sys.exit(2)

    # Run all checks
    result = VerificationResult()

    check_namespace(args.namespace, verbose, result)
    check_deployment(args.namespace, args.release, verbose, result)
    check_pods(args.namespace, args.release, verbose, result)
    check_service(args.namespace, args.release, args.port, verbose, result)
    check_health_endpoint(args.namespace, args.release, args.port, args.timeout, verbose, result)
    check_api_connectivity(args.namespace, args.release, args.api_url, verbose, result)
    check_resource_usage(args.namespace, args.release, verbose, result)

    # Summary
    log("INFO", f"Verification: {result.passed} passed, {result.failed} failed, {result.warnings} warnings", verbose)

    if verbose:
        print("\n--- Verification Results ---")
        for check in result.checks:
            status_symbol = {"PASS": "+", "FAIL": "X", "WARN": "!"}[check["status"]]
            print(f"  [{status_symbol}] {check['name']}: {check['message']}")
        print("")

    if result.success:
        print(f"[OK] Deployment verified ({result.passed} checks passed, {result.warnings} warnings)")
        sys.exit(0)
    else:
        failed_checks = [c for c in result.checks if c["status"] == "FAIL"]
        failed_names = ", ".join(c["name"] for c in failed_checks)
        print(f"[ERROR] Verification failed: {failed_names}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
