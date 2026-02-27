#!/usr/bin/env python3
"""
Generate and deploy all 6 LearnFlow agent microservices.

Creates, builds, deploys, and tests:
  1. triage-agent     - Routes queries
  2. concepts-agent   - Explains topics
  3. code-review-agent - Analyzes code
  4. debug-agent      - Fixes errors
  5. exercise-agent   - Generates problems
  6. progress-agent   - Tracks mastery

Usage:
    python generate_agents.py [--skip-build] [--skip-deploy] [--skip-test] [--namespace default]
"""

import argparse
import os
import subprocess
import sys
import time

# Add scripts directory to path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from create_service import create_service

# ── Agent Definitions ────────────────────────────────────────────────────────

AGENTS = [
    {"name": "triage-agent", "type": "triage"},
    {"name": "concepts-agent", "type": "concepts"},
    {"name": "code-review-agent", "type": "code-review"},
    {"name": "debug-agent", "type": "debug"},
    {"name": "exercise-agent", "type": "exercise"},
    {"name": "progress-agent", "type": "progress"},
]


def run_command(cmd: list, description: str, timeout: int = 300) -> bool:
    """Run a shell command and return success status."""
    print(f"  {description}...")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr or result.stdout}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"  ERROR: Command timed out after {timeout}s")
        return False
    except FileNotFoundError:
        print(f"  ERROR: Command not found: {cmd[0]}")
        return False


def check_prerequisites() -> bool:
    """Validate all prerequisites are available."""
    checks = [
        (["python", "--version"], "Python"),
        (["docker", "--version"], "Docker"),
        (["kubectl", "cluster-info"], "Kubernetes"),
        (["dapr", "--version"], "Dapr CLI"),
    ]

    all_ok = True
    for cmd, name in checks:
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            if result.returncode == 0:
                print(f"  [OK] {name}")
            else:
                print(f"  [FAIL] {name}: not responding")
                all_ok = False
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print(f"  [FAIL] {name}: not found")
            all_ok = False

    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Generate and deploy all LearnFlow agents")
    parser.add_argument("--skip-build", action="store_true", help="Skip Docker build")
    parser.add_argument("--skip-deploy", action="store_true", help="Skip Kubernetes deployment")
    parser.add_argument("--skip-test", action="store_true", help="Skip service tests")
    parser.add_argument("--namespace", default="default", help="Kubernetes namespace")
    args = parser.parse_args()

    print("=" * 60)
    print("LearnFlow Agent Generator")
    print("=" * 60)

    # Prerequisites
    print("\nChecking prerequisites...")
    if not check_prerequisites():
        print("\nERROR: Prerequisites not met. Install missing tools and retry.")
        sys.exit(1)

    start_time = time.time()
    results = {"created": [], "built": [], "deployed": [], "tested": []}
    errors = []

    # ── Phase 1: Create Services ─────────────────────────────────────────────

    print(f"\nPhase 1: Creating {len(AGENTS)} services...")
    for agent in AGENTS:
        try:
            output_dir = create_service(agent["name"], agent["type"])
            results["created"].append(agent["name"])
            print(f"  [OK] {agent['name']} -> {output_dir}")
        except Exception as e:
            errors.append(f"Create {agent['name']}: {e}")
            print(f"  [FAIL] {agent['name']}: {e}")

    # ── Phase 2: Build Docker Images ─────────────────────────────────────────

    if not args.skip_build:
        print(f"\nPhase 2: Building Docker images...")
        for agent in AGENTS:
            if agent["name"] not in results["created"]:
                continue
            build_script = os.path.join(SCRIPT_DIR, "build_docker.sh")
            success = run_command(
                ["bash", build_script, agent["name"]],
                f"Building {agent['name']}",
                timeout=600,
            )
            if success:
                results["built"].append(agent["name"])
            else:
                errors.append(f"Build {agent['name']}")
    else:
        print("\nPhase 2: Skipped (--skip-build)")

    # ── Phase 3: Deploy to Kubernetes ────────────────────────────────────────

    if not args.skip_deploy:
        print(f"\nPhase 3: Deploying to Kubernetes (namespace: {args.namespace})...")

        # Apply Dapr config first
        dapr_config = os.path.join(SCRIPT_DIR, "dapr_config.yaml")
        if os.path.exists(dapr_config):
            run_command(
                ["kubectl", "apply", "-f", dapr_config, "-n", args.namespace],
                "Applying Dapr components",
            )

        for agent in AGENTS:
            if agent["name"] not in results.get("built", results["created"]):
                continue
            deploy_script = os.path.join(SCRIPT_DIR, "deploy_service.sh")
            success = run_command(
                ["bash", deploy_script, agent["name"], args.namespace],
                f"Deploying {agent['name']}",
                timeout=360,
            )
            if success:
                results["deployed"].append(agent["name"])
            else:
                errors.append(f"Deploy {agent['name']}")
    else:
        print("\nPhase 3: Skipped (--skip-deploy)")

    # ── Phase 4: Test Services ───────────────────────────────────────────────

    if not args.skip_test:
        print(f"\nPhase 4: Testing services...")
        for agent in AGENTS:
            if agent["name"] not in results.get("deployed", results["created"]):
                continue
            test_script = os.path.join(SCRIPT_DIR, "test_service.py")
            success = run_command(
                ["python", test_script, agent["name"], args.namespace],
                f"Testing {agent['name']}",
                timeout=120,
            )
            if success:
                results["tested"].append(agent["name"])
            else:
                errors.append(f"Test {agent['name']}")
    else:
        print("\nPhase 4: Skipped (--skip-test)")

    # ── Summary ──────────────────────────────────────────────────────────────

    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Created:  {len(results['created'])}/{len(AGENTS)}")
    if not args.skip_build:
        print(f"  Built:    {len(results['built'])}/{len(AGENTS)}")
    if not args.skip_deploy:
        print(f"  Deployed: {len(results['deployed'])}/{len(AGENTS)}")
    if not args.skip_test:
        print(f"  Tested:   {len(results['tested'])}/{len(AGENTS)}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")

    print(f"\nCompleted in {elapsed:.1f}s")

    if len(results["created"]) == len(AGENTS):
        print(f"All {len(AGENTS)} agents created successfully")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
