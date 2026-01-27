#!/bin/bash
# LearnFlow Platform Deployment Script
# Uses all 7 reusable skills to deploy the complete platform
set -euo pipefail

NAMESPACE="learnflow"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== LearnFlow Platform Deployment ==="
echo "Project: $PROJECT_DIR"
echo ""

# Step 1: Create namespace
echo "[1/7] Creating namespace..."
kubectl apply -f "$PROJECT_DIR/k8s/namespace.yaml"
echo ""

# Step 2: Deploy PostgreSQL (postgres-k8s-setup skill)
echo "[2/7] Deploying PostgreSQL with schema..."
kubectl apply -f "$PROJECT_DIR/k8s/postgres.yaml"
# Apply schema via configmap from database/schema.sql
kubectl create configmap postgres-init-schema \
  --from-file=init.sql="$PROJECT_DIR/database/schema.sql" \
  --namespace=$NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
echo "Waiting for PostgreSQL readiness..."
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s -n $NAMESPACE
echo ""

# Step 3: Deploy Kafka (kafka-k8s-setup skill)
echo "[3/7] Deploying Kafka with topics..."
kubectl apply -f "$PROJECT_DIR/k8s/kafka.yaml"
echo "Waiting for Kafka readiness..."
kubectl wait --for=condition=ready pod -l app=kafka --timeout=180s -n $NAMESPACE
# Apply topic definitions
kubectl apply -f "$PROJECT_DIR/kafka/topics.yaml" -n $NAMESPACE 2>/dev/null || true
echo ""

# Step 4: Deploy Dapr components
echo "[4/7] Configuring Dapr components..."
kubectl apply -f "$PROJECT_DIR/k8s/dapr-components.yaml"
echo ""

# Step 5: Build and deploy agents (fastapi-dapr-agent skill)
echo "[5/7] Deploying 6 microservice agents..."
AGENTS=("triage-agent" "concepts-agent" "code-review-agent" "debug-agent" "exercise-agent" "progress-agent")
AGENT_MODULES=("triage_agent" "concepts_agent" "code_review_agent" "debug_agent" "exercise_agent" "progress_agent")
PORTS=(8000 8001 8002 8003 8004 8005)

for i in "${!AGENTS[@]}"; do
  echo "  Building ${AGENTS[$i]}..."
  docker build -t "learnflow/${AGENTS[$i]}:latest" \
    --build-arg AGENT_MODULE="${AGENT_MODULES[$i]}" \
    --build-arg AGENT_PORT="${PORTS[$i]}" \
    -f "$PROJECT_DIR/Dockerfile.agent" "$PROJECT_DIR"
done

kubectl apply -f "$PROJECT_DIR/k8s/agents.yaml"
echo ""

# Step 6: Deploy code sandbox (mcp-code-execution skill)
echo "[6/7] Deploying code sandbox..."
docker build -t "learnflow/code-sandbox:latest" -f "$PROJECT_DIR/Dockerfile.sandbox" "$PROJECT_DIR"
kubectl apply -f "$PROJECT_DIR/k8s/sandbox.yaml"
echo ""

# Step 7: Deploy frontend (nextjs-k8s-deploy skill)
echo "[7/7] Deploying Next.js frontend..."
docker build -t "learnflow/frontend:latest" -f "$PROJECT_DIR/Dockerfile.frontend" "$PROJECT_DIR"
kubectl apply -f "$PROJECT_DIR/k8s/frontend.yaml"
echo ""

# Wait for all pods
echo "=== Waiting for all pods to be ready ==="
kubectl wait --for=condition=ready pod --all --timeout=300s -n $NAMESPACE
echo ""

echo "=== Deployment Complete ==="
echo "Services:"
kubectl get svc -n $NAMESPACE
echo ""
echo "Pods:"
kubectl get pods -n $NAMESPACE
echo ""
echo "Access frontend at: http://learnflow.local"
