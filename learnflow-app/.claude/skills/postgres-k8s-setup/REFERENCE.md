# postgres-k8s-setup Reference

Complete reference documentation for PostgreSQL Kubernetes deployment.

## Schema Design

### Database: learnflow

The skill initializes the following schema:

```
learnflow/
├── users           # User accounts
├── classes         # Course/class definitions
├── submissions     # Student submissions
├── progress        # Learning progress tracking
├── quizzes         # Quiz definitions
└── __migrations    # Migration tracking (internal)
```

### Table Relationships

```
users (1) ──────< submissions (many)
  │
  └──────────────< progress (many)

classes (1) ────< submissions (many)
  │
  └──────────────< quizzes (many)

quizzes (1) ────< submissions (many)
```

### Indexes

All foreign keys are indexed for query performance:
- `idx_submissions_user_id`
- `idx_submissions_class_id`
- `idx_submissions_quiz_id`
- `idx_progress_user_id`
- `idx_progress_class_id`
- `idx_quizzes_class_id`

## Connection Configuration

### Connection String Format

For application use (e.g., FastAPI):

```python
# Standard format
DATABASE_URL = "postgresql://postgres:password@postgres-postgresql.postgres.svc.cluster.local:5432/learnflow"

# With connection pooling
DATABASE_URL = "postgresql://postgres:password@postgres-postgresql.postgres.svc.cluster.local:5432/learnflow?pool_size=10&max_overflow=20"
```

### Environment Variables

```bash
POSTGRES_HOST=postgres-postgresql.postgres.svc.cluster.local
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<from-secret>
POSTGRES_DB=learnflow
```

### Retrieving Password from Secret

```bash
kubectl get secret postgres-postgresql -n postgres -o jsonpath='{.data.postgres-password}' | base64 -d
```

## Connection Pooling

### Recommended Settings

| Setting | Development | Production |
|---------|-------------|------------|
| pool_size | 5 | 20 |
| max_overflow | 10 | 40 |
| pool_timeout | 30 | 30 |
| pool_recycle | 1800 | 3600 |

### SQLAlchemy Configuration

```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True  # Verify connections
)
```

## Performance Tuning

### Helm Values for Production

```yaml
# values-production.yaml
primary:
  resources:
    requests:
      memory: 2Gi
      cpu: 1000m
    limits:
      memory: 4Gi
      cpu: 2000m

  persistence:
    size: 50Gi
    storageClass: fast-ssd

  extendedConfiguration: |
    max_connections = 200
    shared_buffers = 1GB
    effective_cache_size = 3GB
    maintenance_work_mem = 256MB
    checkpoint_completion_target = 0.9
    wal_buffers = 16MB
    default_statistics_target = 100
    random_page_cost = 1.1
    effective_io_concurrency = 200
    work_mem = 10MB
    min_wal_size = 1GB
    max_wal_size = 4GB
    max_worker_processes = 4
    max_parallel_workers_per_gather = 2
    max_parallel_workers = 4
```

### Query Optimization Tips

1. **Use EXPLAIN ANALYZE** for slow queries
2. **Add indexes** for frequent WHERE clauses
3. **Use connection pooling** to reduce connection overhead
4. **Enable pg_stat_statements** for query monitoring

## Backup & Restore Procedures

### Manual Backup

```bash
# Port-forward to access PostgreSQL
kubectl port-forward svc/postgres-postgresql 5432:5432 -n postgres &

# Create backup
PGPASSWORD=$(kubectl get secret postgres-postgresql -n postgres -o jsonpath='{.data.postgres-password}' | base64 -d) \
pg_dump -h localhost -U postgres -d learnflow -Fc > backup_$(date +%Y%m%d_%H%M%S).dump
```

### Restore from Backup

```bash
# Restore
PGPASSWORD=$POSTGRES_PASSWORD pg_restore -h localhost -U postgres -d learnflow -c backup.dump
```

### Automated Backup Schedule

Create a CronJob for automated backups:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: postgres
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15
            command:
            - /bin/bash
            - -c
            - |
              pg_dump -h postgres-postgresql -U postgres -d learnflow -Fc \
                > /backups/backup_$(date +%Y%m%d_%H%M%S).dump
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-postgresql
                  key: postgres-password
            volumeMounts:
            - name: backup-storage
              mountPath: /backups
          restartPolicy: OnFailure
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: postgres-backups
```

## Troubleshooting

### Problem: "kubectl not found"

**Cause**: kubectl not installed or not in PATH.

**Solution**:
```bash
# Install kubectl (Linux)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify
kubectl version --client
```

### Problem: "Kubernetes not accessible"

**Cause**: No cluster configured or cluster unreachable.

**Solution**:
```bash
# Check current context
kubectl config current-context

# List available contexts
kubectl config get-contexts

# Switch context
kubectl config use-context my-cluster

# Test connectivity
kubectl cluster-info
```

### Problem: "Pod stuck in Pending"

**Cause**: Insufficient resources or no available nodes.

**Solution**:
```bash
# Check pod events
kubectl describe pod -l app.kubernetes.io/name=postgresql -n postgres

# Check node resources
kubectl top nodes

# Check PVC status
kubectl get pvc -n postgres
```

### Problem: "Connection refused"

**Cause**: Pod not ready or service misconfigured.

**Solution**:
```bash
# Check pod status
kubectl get pods -n postgres

# Check service endpoints
kubectl get endpoints postgres-postgresql -n postgres

# Test from within cluster
kubectl run pg-test --rm -it --image=postgres:15 -- psql -h postgres-postgresql.postgres.svc.cluster.local -U postgres
```

### Problem: "Authentication failed"

**Cause**: Wrong password or user.

**Solution**:
```bash
# Get correct password
kubectl get secret postgres-postgresql -n postgres -o jsonpath='{.data.postgres-password}' | base64 -d

# Verify secret exists
kubectl get secrets -n postgres
```

### Problem: "Migration failed"

**Cause**: SQL syntax error or constraint violation.

**Solution**:
```bash
# Check migration logs
cat scripts/.postgres-deploy.log

# Run migration manually to see error
PGPASSWORD=$PASSWORD psql -h localhost -U postgres -d learnflow -f migrations/M001_initial.sql

# Check __migrations table
psql -c "SELECT * FROM __migrations ORDER BY applied_at DESC LIMIT 5"
```

### Problem: "Helm install timeout"

**Cause**: Slow cluster or large PVC provisioning.

**Solution**:
```bash
# Increase timeout
helm install postgres bitnami/postgresql \
  --namespace postgres \
  --timeout 10m \
  --wait

# Check helm status
helm status postgres -n postgres

# Check events
kubectl get events -n postgres --sort-by='.lastTimestamp'
```

## Integration Examples

### FastAPI Integration

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL",
    "postgresql://postgres:password@postgres-postgresql.postgres.svc.cluster.local:5432/learnflow")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Dapr State Store Configuration

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: postgres-connection
      key: connection-string
  - name: tableName
    value: "dapr_state"
```

### Kafka Connect (for CDC)

```json
{
  "name": "postgres-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres-postgresql.postgres.svc.cluster.local",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "${secrets:postgres-password}",
    "database.dbname": "learnflow",
    "topic.prefix": "learnflow",
    "plugin.name": "pgoutput"
  }
}
```

## Helm Chart Configuration

### Default Values Used

```yaml
# Bitnami PostgreSQL 12.x defaults
global:
  postgresql:
    auth:
      postgresPassword: ""  # Auto-generated
      database: "learnflow"

primary:
  persistence:
    enabled: true
    size: 8Gi

  resources:
    requests:
      memory: 256Mi
      cpu: 250m

metrics:
  enabled: false  # Enable for production monitoring
```

### Custom Values Example

```bash
helm install postgres bitnami/postgresql \
  --namespace postgres \
  --set auth.database=learnflow \
  --set primary.persistence.size=20Gi \
  --set primary.resources.requests.memory=1Gi \
  --set metrics.enabled=true
```

## Monitoring

### Enable Prometheus Metrics

```bash
helm upgrade postgres bitnami/postgresql \
  --namespace postgres \
  --set metrics.enabled=true \
  --set metrics.serviceMonitor.enabled=true
```

### Key Metrics to Monitor

- `pg_stat_activity_count` - Active connections
- `pg_stat_database_tup_fetched` - Rows read
- `pg_stat_database_tup_inserted` - Rows inserted
- `pg_stat_database_deadlocks` - Deadlock count
- `pg_replication_lag` - Replication lag (if replicas enabled)
