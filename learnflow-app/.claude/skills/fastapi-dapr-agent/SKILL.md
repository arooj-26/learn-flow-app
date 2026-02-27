---
name: fastapi-dapr-agent
description: Generate FastAPI microservices with Dapr sidecar for event-driven architecture
allowed-tools: [python, bash]
---

# fastapi-dapr-agent

Generate and deploy FastAPI microservices with Dapr sidecar integration for event-driven, AI-powered learning agents.

## Quick Start

```bash
# Create a single service
python scripts/create_service.py --name triage-agent --type triage

# Build Docker image
bash scripts/build_docker.sh triage-agent

# Deploy to Kubernetes
bash scripts/deploy_service.sh triage-agent

# Test deployment
python scripts/test_service.py triage-agent

# Generate and deploy all 6 agents
python scripts/generate_agents.py
```

## Services

| Agent | Purpose | Topic |
|-------|---------|-------|
| triage-agent | Routes queries to correct agent | learning.submitted |
| concepts-agent | Explains topics | learning.concepts |
| code-review-agent | Analyzes code | learning.review |
| debug-agent | Fixes errors | learning.debug |
| exercise-agent | Generates problems | learning.exercise |
| progress-agent | Tracks mastery | learning.progress |

## Dapr Components

- **State store**: PostgreSQL (`postgres`)
- **Pub/sub**: Kafka (`kafka`)
- **Invocation**: Direct service-to-service via Dapr

## Prerequisites

- Python 3.8+
- Docker
- Kubernetes cluster (accessible via kubectl)
- Dapr CLI installed and initialized
