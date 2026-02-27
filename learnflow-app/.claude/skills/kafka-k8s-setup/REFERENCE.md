# kafka-k8s-setup Reference

Complete reference documentation for Kafka Kubernetes deployment.

## Topic Configuration

### LearnFlow Topics

The skill creates 4 topics for the LearnFlow learning platform:

#### learning.submitted
- **Purpose**: Tracks when students submit assignments or quizzes
- **Partitions**: 3 (allows parallel processing)
- **Retention**: 7 days
- **Key**: `user_id` (ensures ordering per student)

Message schema:
```json
{
  "event_type": "submission",
  "user_id": "uuid",
  "class_id": "uuid",
  "quiz_id": "uuid",
  "submitted_at": "2024-01-15T10:30:00Z",
  "score": 85.5
}
```

#### code.executed
- **Purpose**: Tracks code execution events for learning analytics
- **Partitions**: 3
- **Retention**: 7 days
- **Key**: `session_id`

Message schema:
```json
{
  "event_type": "code_execution",
  "user_id": "uuid",
  "session_id": "uuid",
  "language": "python",
  "execution_time_ms": 150,
  "success": true,
  "error": null
}
```

#### exercise.started
- **Purpose**: Tracks when students begin exercises
- **Partitions**: 3
- **Retention**: 7 days
- **Key**: `user_id`

Message schema:
```json
{
  "event_type": "exercise_started",
  "user_id": "uuid",
  "exercise_id": "uuid",
  "started_at": "2024-01-15T10:00:00Z"
}
```

#### struggle.detected
- **Purpose**: AI-detected learning struggles for intervention
- **Partitions**: 3
- **Retention**: 3 days (shorter - actionable alerts)
- **Key**: `user_id`

Message schema:
```json
{
  "event_type": "struggle_detected",
  "user_id": "uuid",
  "struggle_type": "repeated_errors",
  "confidence": 0.85,
  "recommended_action": "offer_hint",
  "detected_at": "2024-01-15T10:25:00Z"
}
```

## Consumer Group Management

### Best Practices

1. **Naming Convention**: `{service}-{environment}-{purpose}`
   - Example: `analytics-prod-submissions`
   - Example: `notifications-dev-struggles`

2. **Partition Assignment**:
   - Consumers = Partitions for maximum parallelism
   - 3 partitions → 3 consumer instances optimal

3. **Offset Management**:
   - Use `auto.offset.reset=earliest` for replay capability
   - Commit offsets after processing, not before

### Consumer Configuration

```python
consumer_config = {
    'bootstrap.servers': 'kafka-headless.kafka.svc.cluster.local:9092',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,  # Manual commit recommended
    'session.timeout.ms': 30000,
    'heartbeat.interval.ms': 10000,
    'max.poll.interval.ms': 300000,
}
```

### Reset Consumer Group Offset

```bash
# Reset to earliest
kubectl exec -n kafka kafka-0 -- kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group my-group \
  --topic learning.submitted \
  --reset-offsets --to-earliest --execute

# Reset to specific offset
kubectl exec -n kafka kafka-0 -- kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group my-group \
  --topic learning.submitted \
  --reset-offsets --to-offset 100 --execute
```

## Performance Tuning

### Producer Configuration

```python
producer_config = {
    'bootstrap.servers': 'kafka-headless.kafka.svc.cluster.local:9092',
    'acks': 'all',  # Wait for all replicas
    'retries': 3,
    'retry.backoff.ms': 100,
    'batch.size': 16384,
    'linger.ms': 5,  # Small delay for batching
    'buffer.memory': 33554432,
    'compression.type': 'lz4',
}
```

### Helm Values for Production

```yaml
# values-production.yaml
replicaCount: 3

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

config:
  log.retention.hours: 168  # 7 days
  log.segment.bytes: 1073741824  # 1GB
  num.partitions: 3
  default.replication.factor: 2
  min.insync.replicas: 1
  auto.create.topics.enable: false

zookeeper:
  replicaCount: 3
  resources:
    requests:
      memory: 512Mi
      cpu: 250m
```

### Topic-Level Tuning

```bash
# Increase partitions for high-throughput topic
kubectl exec -n kafka kafka-0 -- kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --alter --topic learning.submitted \
  --partitions 6

# Adjust retention
kubectl exec -n kafka kafka-0 -- kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --alter --entity-type topics --entity-name struggle.detected \
  --add-config retention.ms=259200000  # 3 days
```

## Monitoring

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `kafka_consumer_lag` | Messages behind | > 10000 |
| `kafka_request_rate` | Requests/sec | > 10000 |
| `kafka_under_replicated_partitions` | Unhealthy partitions | > 0 |
| `kafka_offline_partitions` | Unavailable partitions | > 0 |
| `kafka_network_io` | Network throughput | > 80% capacity |

### Enable Prometheus Metrics

```bash
helm upgrade kafka bitnami/kafka \
  --namespace kafka \
  --set metrics.kafka.enabled=true \
  --set metrics.jmx.enabled=true \
  --set metrics.serviceMonitor.enabled=true
```

### View Consumer Lag

```bash
kubectl exec -n kafka kafka-0 -- kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group my-consumer-group
```

## Troubleshooting

### Problem: "Kafka pod not starting"

**Cause**: Insufficient memory or Zookeeper not ready.

**Solution**:
```bash
# Check pod events
kubectl describe pod -l app.kubernetes.io/name=kafka -n kafka

# Check Zookeeper first
kubectl get pods -l app.kubernetes.io/name=zookeeper -n kafka

# Check resource usage
kubectl top pods -n kafka

# Check logs
kubectl logs -l app.kubernetes.io/name=kafka -n kafka --tail=50
```

### Problem: "Cannot connect to Kafka"

**Cause**: Service not exposed or wrong address.

**Solution**:
```bash
# Verify service exists
kubectl get svc -n kafka

# Internal address (from within cluster)
# kafka-headless.kafka.svc.cluster.local:9092

# Port-forward for local testing
kubectl port-forward svc/kafka 9092:9092 -n kafka

# Test connection from within cluster
kubectl run kafka-test --rm -it --image=bitnami/kafka:latest -- \
  kafka-topics.sh --bootstrap-server kafka.kafka.svc.cluster.local:9092 --list
```

### Problem: "Topic creation failed"

**Cause**: Kafka not ready or insufficient replicas.

**Solution**:
```bash
# Check Kafka is ready
kubectl exec -n kafka kafka-0 -- kafka-broker-api-versions.sh \
  --bootstrap-server localhost:9092

# List brokers
kubectl exec -n kafka kafka-0 -- kafka-metadata.sh \
  --snapshot /bitnami/kafka/data/__cluster_metadata-0/00000000000000000000.log \
  --command "broker"

# Create topic manually
kubectl exec -n kafka kafka-0 -- kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --topic test \
  --partitions 3 --replication-factor 1 \
  --if-not-exists
```

### Problem: "Consumer not receiving messages"

**Cause**: Wrong offset, topic doesn't exist, or consumer group issue.

**Solution**:
```bash
# Check topic exists
kubectl exec -n kafka kafka-0 -- kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe --topic learning.submitted

# Check consumer group
kubectl exec -n kafka kafka-0 -- kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group my-group

# Console consumer test
kubectl exec -n kafka kafka-0 -- kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic learning.submitted \
  --from-beginning --max-messages 5
```

### Problem: "High consumer lag"

**Cause**: Consumers too slow or too few instances.

**Solution**:
```bash
# Check lag
kubectl exec -n kafka kafka-0 -- kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group my-group

# Scale consumers (if using Deployment)
kubectl scale deployment my-consumer --replicas=3

# Reset to latest (skip backlog - data loss!)
kubectl exec -n kafka kafka-0 -- kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group my-group --topic learning.submitted \
  --reset-offsets --to-latest --execute
```

### Problem: "Helm install timeout"

**Cause**: Slow PVC provisioning or insufficient resources.

**Solution**:
```bash
# Increase timeout
helm install kafka bitnami/kafka \
  --namespace kafka \
  --timeout 10m \
  --wait

# Check events
kubectl get events -n kafka --sort-by='.lastTimestamp'

# Check PVC status
kubectl get pvc -n kafka

# Check storage class
kubectl get storageclass
```

## Integration Examples

### FastAPI with Dapr

```python
# producer.py
from dapr.clients import DaprClient

async def publish_submission(submission: dict):
    with DaprClient() as client:
        client.publish_event(
            pubsub_name="kafka-pubsub",
            topic_name="learning.submitted",
            data=json.dumps(submission),
            data_content_type="application/json"
        )
```

Dapr Component:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-headless.kafka.svc.cluster.local:9092"
  - name: consumerGroup
    value: "learnflow-api"
  - name: authType
    value: "none"
```

### Direct Python Client

```python
from confluent_kafka import Producer, Consumer
import json

# Producer
producer = Producer({
    'bootstrap.servers': 'kafka-headless.kafka.svc.cluster.local:9092'
})

def publish(topic: str, message: dict, key: str = None):
    producer.produce(
        topic,
        value=json.dumps(message).encode('utf-8'),
        key=key.encode('utf-8') if key else None
    )
    producer.flush()

# Consumer
consumer = Consumer({
    'bootstrap.servers': 'kafka-headless.kafka.svc.cluster.local:9092',
    'group.id': 'my-service',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['learning.submitted'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Error: {msg.error()}")
        continue

    data = json.loads(msg.value().decode('utf-8'))
    process_message(data)
    consumer.commit()
```

## Helm Chart Configuration

### Default Values Used

```yaml
# Bitnami Kafka 28.x
replicaCount: 1

listeners:
  client:
    protocol: PLAINTEXT
  controller:
    protocol: PLAINTEXT
  interbroker:
    protocol: PLAINTEXT

controller:
  replicaCount: 1

persistence:
  enabled: true
  size: 8Gi

zookeeper:
  enabled: true
  replicaCount: 1
```

### KRaft Mode (No Zookeeper)

```bash
helm install kafka bitnami/kafka \
  --namespace kafka \
  --set kraft.enabled=true \
  --set zookeeper.enabled=false \
  --set controller.replicaCount=3
```

## Security (Production)

### Enable SASL/SCRAM

```yaml
# values-secure.yaml
auth:
  clientProtocol: sasl
  interBrokerProtocol: sasl
  sasl:
    mechanism: scram-sha-256
    jaas:
      clientUsers:
        - user1
      clientPasswords:
        - password1

listeners:
  client:
    protocol: SASL_PLAINTEXT
  interbroker:
    protocol: SASL_PLAINTEXT
```

### TLS Encryption

```yaml
tls:
  enabled: true
  existingSecret: kafka-tls-secret

listeners:
  client:
    protocol: SASL_SSL
```

## Backup & Recovery

### Topic Configuration Backup

```bash
# Export topic configs
kubectl exec -n kafka kafka-0 -- kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe > topics-backup.txt

# Export consumer group offsets
kubectl exec -n kafka kafka-0 -- kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --all-groups --describe > consumer-groups-backup.txt
```

### Data Backup (via MirrorMaker)

For full data backup, use Kafka MirrorMaker 2 to replicate to backup cluster.
