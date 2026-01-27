---
name: postgres-k8s-setup
description: Deploy PostgreSQL to Kubernetes with idempotent schema initialization
version: 1.0.0
allowed-tools:
  - Bash(kubectl*)
  - Bash(helm*)
  - Bash(psql*)
  - Bash(python*)
  - Bash(bash*)
  - Read
  - Write
---

# postgres-k8s-setup

Deploy PostgreSQL to Kubernetes with schema initialization and zero token waste.

## When to Use

Use this skill when:
- Setting up PostgreSQL for a new Kubernetes-based application
- Initializing database schema for LearnFlow or similar projects
- Running database migrations in a Kubernetes environment
- Need idempotent, repeatable database deployment

## Prerequisites

Before running, ensure:
- `kubectl` installed and in PATH
- Kubernetes cluster accessible (`kubectl cluster-info` works)
- `helm` 3.9+ installed
- `psql` client available (for verification)
- Minimum 2GB available memory in cluster

## Instructions

### Deploy PostgreSQL

```bash
# Full deployment with schema
bash skills/postgres-k8s-setup/scripts/deploy.sh

# Deploy with custom namespace
NAMESPACE=myapp bash skills/postgres-k8s-setup/scripts/deploy.sh

# Debug mode
DEBUG=1 bash skills/postgres-k8s-setup/scripts/deploy.sh
```

### Run Migrations

```bash
# Apply pending migrations
python skills/postgres-k8s-setup/scripts/run_migrations.py

# Dry run (show what would run)
python skills/postgres-k8s-setup/scripts/run_migrations.py --dry-run
```

### Verify Deployment

```bash
# Run all 5 verification tests
python skills/postgres-k8s-setup/scripts/verify.py

# Verbose output
python skills/postgres-k8s-setup/scripts/verify.py --verbose
```

### Backup Database

```bash
# Create backup
python skills/postgres-k8s-setup/scripts/backup.py

# Backup specific database
python skills/postgres-k8s-setup/scripts/backup.py --database learnflow
```

### Rollback/Cleanup

```bash
# Remove deployment (keeps PVC data)
bash skills/postgres-k8s-setup/scripts/rollback.sh

# Full cleanup including data
bash skills/postgres-k8s-setup/scripts/rollback.sh --delete-pvc
```

## Validation Checklist

- [ ] kubectl accessible
- [ ] Kubernetes cluster reachable
- [ ] Helm 3+ installed
- [ ] psql client available
- [ ] Sufficient cluster resources

## Success Criteria

Output on successful deployment:
```
[OK] PostgreSQL deployed (host: postgres-postgresql.postgres.svc.cluster.local, port: 5432)
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
| Connection test | 30 seconds | 10 seconds |
| Query execution | 10 seconds | - |

## Token Efficiency

This skill follows the MCP token efficiency pattern:
- Heavy operations in external scripts
- Filtered responses (no full JSON dumps)
- Minimal output: "[OK] PostgreSQL deployed" (~15 tokens)
