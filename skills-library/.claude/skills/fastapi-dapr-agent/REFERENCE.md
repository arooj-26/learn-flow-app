# FastAPI-Dapr Agent Reference

## Dapr Component Configuration

### State Store (PostgreSQL)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgres
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      value: "host=postgres-svc;port=5432;user=dapr;password=dapr;database=learnflow;sslmode=disable"
    - name: actorStateStore
      value: "true"
```

### Pub/Sub (Kafka)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka-svc:9092"
    - name: consumerGroup
      value: "learnflow-agents"
    - name: authType
      value: "none"
```

## Pub/Sub Patterns

### Publishing Events

```python
from dapr.clients import DaprClient

async def publish_event(topic: str, data: dict):
    with DaprClient() as client:
        client.publish_event(
            pubsub_name="kafka",
            topic_name=topic,
            data=json.dumps(data),
            data_content_type="application/json"
        )
```

### Subscribing to Events

```python
from dapr.ext.fastapi import DaprApp

dapp = DaprApp(app)

@dapp.subscribe(pubsub_name="kafka", topic="learning.submitted")
async def on_event(msg: Any) -> None:
    payload = json.loads(msg.body)
    # Process event
```

### Topic Routing

| Source | Topic | Target |
|--------|-------|--------|
| Client | learning.submitted | triage-agent |
| Triage | learning.concepts | concepts-agent |
| Triage | learning.review | code-review-agent |
| Triage | learning.debug | debug-agent |
| Triage | learning.exercise | exercise-agent |
| Any | learning.progress | progress-agent |

## State Management

### Save State

```python
from dapr.clients import DaprClient

def save_state(store: str, key: str, value: dict):
    with DaprClient() as client:
        client.save_state(store, key, json.dumps(value))
```

### Get State

```python
def get_state(store: str, key: str) -> dict:
    with DaprClient() as client:
        data = client.get_state(store, key)
        return json.loads(data.data) if data.data else {}
```

### Delete State

```python
def delete_state(store: str, key: str):
    with DaprClient() as client:
        client.delete_state(store, key)
```

## Service Invocation

### Direct Invocation (Service-to-Service)

```python
from dapr.clients import DaprClient

def invoke_service(app_id: str, method: str, data: dict) -> dict:
    with DaprClient() as client:
        response = client.invoke_method(
            app_id=app_id,
            method_name=method,
            data=json.dumps(data),
            content_type="application/json"
        )
        return json.loads(response.data)
```

### Example: Triage routing to Concepts

```python
result = invoke_service("concepts-agent", "explain", {
    "topic": "recursion",
    "level": "beginner"
})
```

## Troubleshooting

### 1. Dapr Sidecar Not Starting

**Symptom**: Pod stuck in `Init:0/1` or sidecar container CrashLoopBackOff.

**Fix**:
```bash
# Check Dapr is initialized in cluster
dapr status -k
# Re-initialize if needed
dapr init -k
# Check sidecar logs
kubectl logs <pod> -c daprd
```

### 2. Pub/Sub Messages Not Delivered

**Symptom**: Published events never reach subscriber.

**Fix**:
```bash
# Verify Kafka broker is accessible
kubectl exec -it kafka-0 -- kafka-topics.sh --list --bootstrap-server localhost:9092
# Check component is loaded
dapr components -k
# Check subscription endpoint returns correct routes
curl http://localhost:<dapr-port>/dapr/subscribe
```

### 3. State Store Connection Failed

**Symptom**: `500 Internal Server Error` on state save/get.

**Fix**:
```bash
# Verify PostgreSQL is running
kubectl get pods -l app=postgres
# Test connection
kubectl exec -it postgres-0 -- psql -U dapr -d learnflow -c "SELECT 1"
# Check component config
kubectl get component postgres -o yaml
```

### 4. Port Conflict on Local Development

**Symptom**: `Address already in use` when starting FastAPI.

**Fix**:
```bash
# Find process on port
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows
# Kill or use different port
uvicorn main:app --port 8001
```

### 5. Docker Build Fails

**Symptom**: `pip install` fails during Docker build.

**Fix**:
```bash
# Ensure requirements.txt is valid
pip install -r requirements.txt --dry-run
# Check Python version compatibility
python --version
# Rebuild without cache
docker build --no-cache -t <service> .
```

### 6. Service Invocation Timeout

**Symptom**: `context deadline exceeded` on service-to-service calls.

**Fix**:
```bash
# Check target service is running
kubectl get pods -l app=<target-service>
# Verify Dapr app-id annotation matches
kubectl get pod <pod> -o jsonpath='{.metadata.annotations}'
# Check network policies
kubectl get networkpolicy
```

## Performance Guidelines

- Keep health check response < 50ms
- Pub/sub handler should acknowledge within 10s
- State operations should complete within 2s
- Service invocation timeout default: 60s
- Use async handlers for all I/O-bound operations
