#!/usr/bin/env python3
"""
Create a single FastAPI + Dapr microservice.

Usage:
    python create_service.py --name triage-agent --type triage
    python create_service.py --name concepts-agent --type concepts
"""

import argparse
import os
import re
import sys

from service_template import (
    AGENT_CODE,
    DOCKERFILE_TEMPLATE,
    K8S_MANIFEST_TEMPLATE,
    REQUIREMENTS_TEMPLATE,
    SERVICE_TEMPLATE,
)

VALID_TYPES = list(AGENT_CODE.keys())

DISPLAY_NAMES = {
    "triage": "Triage Agent",
    "concepts": "Concepts Agent",
    "code-review": "Code Review Agent",
    "debug": "Debug Agent",
    "exercise": "Exercise Agent",
    "progress": "Progress Agent",
}

DESCRIPTIONS = {
    "triage": "routing learning queries to the correct specialist agent",
    "concepts": "explaining topics and concepts to learners",
    "code-review": "analyzing and reviewing code submissions",
    "debug": "diagnosing and fixing code errors",
    "exercise": "generating practice problems and evaluating solutions",
    "progress": "tracking learner mastery and progress metrics",
}


def validate_service_name(name: str) -> bool:
    """Validate service name follows Kubernetes naming conventions."""
    pattern = r"^[a-z][a-z0-9\-]{1,61}[a-z0-9]$"
    return bool(re.match(pattern, name))


def create_service(name: str, agent_type: str, output_dir: str = None) -> str:
    """Create a FastAPI + Dapr service from template."""
    if not validate_service_name(name):
        print(f"ERROR: Invalid service name '{name}'. Must match: ^[a-z][a-z0-9-]{{1,61}}[a-z0-9]$")
        sys.exit(1)

    if agent_type not in VALID_TYPES:
        print(f"ERROR: Invalid agent type '{agent_type}'. Valid types: {VALID_TYPES}")
        sys.exit(1)

    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "services", name)

    os.makedirs(output_dir, exist_ok=True)

    display_name = DISPLAY_NAMES.get(agent_type, name.replace("-", " ").title())
    description = DESCRIPTIONS.get(agent_type, f"handling {agent_type} tasks")
    agent_code = AGENT_CODE[agent_type]

    # Generate main.py
    main_code = SERVICE_TEMPLATE.format(
        service_name=name,
        service_display_name=display_name,
        service_description=description,
        agent_specific_code=agent_code,
    )
    with open(os.path.join(output_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_code)

    # Generate Dockerfile
    with open(os.path.join(output_dir, "Dockerfile"), "w", encoding="utf-8") as f:
        f.write(DOCKERFILE_TEMPLATE)

    # Generate requirements.txt
    with open(os.path.join(output_dir, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(REQUIREMENTS_TEMPLATE)

    # Generate Kubernetes manifest
    k8s_dir = os.path.join(output_dir, "k8s")
    os.makedirs(k8s_dir, exist_ok=True)
    manifest = K8S_MANIFEST_TEMPLATE.format(service_name=name)
    with open(os.path.join(k8s_dir, "deployment.yaml"), "w", encoding="utf-8") as f:
        f.write(manifest)

    return output_dir


def main():
    parser = argparse.ArgumentParser(description="Create a FastAPI + Dapr microservice")
    parser.add_argument("--name", required=True, help="Service name (e.g., triage-agent)")
    parser.add_argument("--type", required=True, dest="agent_type", choices=VALID_TYPES,
                        help=f"Agent type: {VALID_TYPES}")
    parser.add_argument("--output", default=None, help="Output directory (default: ./services/<name>)")
    args = parser.parse_args()

    output_dir = create_service(args.name, args.agent_type, args.output)
    print(f"Service {args.name} created at {output_dir}")


if __name__ == "__main__":
    main()
