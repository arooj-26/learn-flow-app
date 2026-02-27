---
name: kafka-k8s-setup
description: Deploy Kafka to Kubernetes with topic management and pub/sub verification
version: 1.0.0
allowed-tools:
  - Bash(kubectl*)
  - Bash(helm*)
  - Bash(python*)
  - Bash(bash*)
  - Read
  - Write
---

# kafka-k8s-setup

Deploy Apache Kafka to Kubernetes with topic management and zero token waste.

## When to Use

Use this skill when:
- Setting up Kafka for event-driven microservices
- Creating topics for LearnFlow learning events
- Verifying pub/sub functionality in Kubernetes
- Need idempotent, repeatable Kafka deployment

## Prerequisites

Before running, ensure:
- `kubectl` installed and in PATH
- Kubernetes cluster accessible
- `helm` 3.9+ installed
- At least 4GB available memory in cluster
- Sufficient pod quotas for 3+ pods

## Instructions

### Deploy Kafka

```bash
# Full deployment
bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh

# Deploy with custom namespace
NAMESPACE=myapp bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh

# Debug mode
DEBUG=1 bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh
```

### Create Topics

```bash
# Create all required topics
python .claude/skills/kafka-k8s-setup/scripts/create_topics.py

# Dry run
python .claude/skills/kafka-k8s-setup/scripts/create_topics.py --dry-run

# List existing topics
python .claude/skills/kafka-k8s-setup/scripts/create_topics.py --list-only
```

### Verify Deployment

```bash
# Run all 5 verification tests
python .claude/skills/kafka-k8s-setup/scripts/verify.py

# Verbose output
python .claude/skills/kafka-k8s-setup/scripts/verify.py --verbose
```

### Test Pub/Sub

```bash
# Test publish and consume
python .claude/skills/kafka-k8s-setup/scripts/test_publish.py

# Test specific topic
python .claude/skills/kafka-k8s-setup/scripts/test_publish.py --topic learning.submitted
```

### Cleanup

```bash
# Remove Kafka deployment
bash .claude/skills/kafka-k8s-setup/scripts/cleanup.sh

# Force cleanup (no confirmation)
bash .claude/skills/kafka-k8s-setup/scripts/cleanup.sh --force
```

## Topic Specifications

| Topic | Partitions | Replicas | Retention |
|-------|------------|----------|-----------|
| `learning.submitted` | 3 | 1 | 7 days |
| `code.executed` | 3 | 1 | 7 days |
| `exercise.started` | 3 | 1 | 7 days |
| `struggle.detected` | 3 | 1 | 3 days |

## Validation Checklist

- [ ] kubectl accessible
- [ ] Kubernetes cluster reachable
- [ ] Helm 3+ installed
- [ ] Sufficient cluster memory (4GB+)
- [ ] Pod quotas allow 3+ pods

## Success Criteria

Output on successful deployment:
```
[OK] Kafka deployed (brokers: 1, zookeeper: 1)
```

Output on successful verification:
```
[OK] All 5 tests passed
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Fatal error (deployment failed, tests failed) |
| 2 | Prerequisites not met (retryable) |

## Timing Specifications

| Operation | Timeout | Retry Interval |
|-----------|---------|----------------|
| Helm install | 5 minutes | 30 seconds |
| Pod startup | 5 minutes | 10 seconds |
| Topic creation | 30 seconds | 5 seconds |
| Pub/sub test | 30 seconds | - |

## Token Efficiency

This skill follows the MCP token efficiency pattern:
- Heavy operations in external scripts
- Filtered responses (no full topic configs)
- Minimal output: "[OK] Kafka deployed" (~15 tokens)
