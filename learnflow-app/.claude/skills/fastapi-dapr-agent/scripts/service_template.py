"""
Base service template for FastAPI + Dapr microservices.
Used by create_service.py and generate_agents.py to produce agent services.
"""

SERVICE_TEMPLATE = '''"""
{service_display_name} - LearnFlow Agent
FastAPI + Dapr microservice for {service_description}
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dapr.ext.fastapi import DaprApp
from dapr.clients import DaprClient

# ── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("{service_name}")

# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="{service_display_name}",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

dapp = DaprApp(app)

# ── Constants ────────────────────────────────────────────────────────────────

STATE_STORE = os.getenv("STATE_STORE", "postgres")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "kafka")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# ── Request/Response Logging Middleware ──────────────────────────────────────

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = datetime.utcnow()
    logger.info("REQ %s %s", request.method, request.url.path)
    response = await call_next(request)
    elapsed = (datetime.utcnow() - start).total_seconds() * 1000
    logger.info("RES %s %s %d %.1fms", request.method, request.url.path, response.status_code, elapsed)
    return response

# ── Health ───────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {{
        "status": "healthy",
        "service": "{service_name}",
        "timestamp": datetime.now().isoformat(),
    }}

@app.get("/ready")
async def readiness():
    """Readiness probe - checks Dapr sidecar connectivity."""
    try:
        with DaprClient() as client:
            client.wait(10)
        return {{"status": "ready"}}
    except Exception as e:
        logger.error("Readiness check failed: %s", e)
        raise HTTPException(status_code=503, detail="Dapr sidecar not ready")

# ── State Management Helpers ─────────────────────────────────────────────────

def save_state(key: str, value: dict) -> None:
    """Save state to Dapr state store."""
    try:
        with DaprClient() as client:
            client.save_state(STATE_STORE, key, json.dumps(value))
        logger.debug("State saved: %s", key)
    except Exception as e:
        logger.error("Failed to save state %s: %s", key, e)
        raise

def get_state(key: str) -> Optional[dict]:
    """Retrieve state from Dapr state store."""
    try:
        with DaprClient() as client:
            data = client.get_state(STATE_STORE, key)
            if data.data:
                return json.loads(data.data)
            return None
    except Exception as e:
        logger.error("Failed to get state %s: %s", key, e)
        raise

def delete_state(key: str) -> None:
    """Delete state from Dapr state store."""
    try:
        with DaprClient() as client:
            client.delete_state(STATE_STORE, key)
        logger.debug("State deleted: %s", key)
    except Exception as e:
        logger.error("Failed to delete state %s: %s", key, e)
        raise

# ── Pub/Sub Helpers ──────────────────────────────────────────────────────────

async def publish_event(topic: str, data: dict) -> None:
    """Publish an event to a Kafka topic via Dapr."""
    try:
        with DaprClient() as client:
            client.publish_event(
                pubsub_name=PUBSUB_NAME,
                topic_name=topic,
                data=json.dumps(data),
                data_content_type="application/json",
            )
        logger.info("Published to %s: %s", topic, list(data.keys()))
    except Exception as e:
        logger.error("Failed to publish to %s: %s", topic, e)
        raise

# ── Service Invocation Helper ────────────────────────────────────────────────

def invoke_service(app_id: str, method: str, data: dict) -> dict:
    """Invoke another Dapr service directly."""
    try:
        with DaprClient() as client:
            response = client.invoke_method(
                app_id=app_id,
                method_name=method,
                data=json.dumps(data),
                content_type="application/json",
            )
            return json.loads(response.data)
    except Exception as e:
        logger.error("Failed to invoke %s/%s: %s", app_id, method, e)
        raise

{agent_specific_code}

# ── Startup ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
'''

# ── Agent-Specific Code Blocks ───────────────────────────────────────────────

AGENT_CODE = {
    "triage": '''
# ── Triage Agent: Routes queries to the correct agent ────────────────────────

from pydantic import BaseModel

class LearningQuery(BaseModel):
    user_id: str
    query: str
    context: Optional[str] = None

ROUTING_MAP = {
    "explain": "learning.concepts",
    "concept": "learning.concepts",
    "what is": "learning.concepts",
    "how does": "learning.concepts",
    "review": "learning.review",
    "code review": "learning.review",
    "analyze": "learning.review",
    "debug": "learning.debug",
    "fix": "learning.debug",
    "error": "learning.debug",
    "exercise": "learning.exercise",
    "practice": "learning.exercise",
    "problem": "learning.exercise",
    "progress": "learning.progress",
    "mastery": "learning.progress",
    "stats": "learning.progress",
}

def classify_query(query: str) -> str:
    """Classify a query to determine which agent should handle it."""
    query_lower = query.lower()
    for keyword, topic in ROUTING_MAP.items():
        if keyword in query_lower:
            return topic
    return "learning.concepts"  # default

@app.post("/route")
async def route_query(query: LearningQuery):
    """Route a learning query to the appropriate agent."""
    topic = classify_query(query.query)
    event_data = {
        "user_id": query.user_id,
        "query": query.query,
        "context": query.context,
        "routed_at": datetime.now().isoformat(),
        "source": "triage-agent",
    }
    await publish_event(topic, event_data)
    save_state(f"triage:{query.user_id}:latest", event_data)
    logger.info("Routed query to %s for user %s", topic, query.user_id)
    return {"status": "routed", "topic": topic, "user_id": query.user_id}

@dapp.subscribe(pubsub_name="kafka", topic="learning.submitted")
async def on_learning_submitted(msg: Any) -> Response:
    """Handle incoming learning queries from pub/sub."""
    try:
        payload = json.loads(msg.body) if isinstance(msg.body, (str, bytes)) else msg.body
        query = LearningQuery(**payload)
        result = await route_query(query)
        logger.info("Processed submitted query: %s", result)
        return Response(status_code=200)
    except Exception as e:
        logger.error("Failed to process submitted query: %s", e)
        return Response(status_code=500)
''',

    "concepts": '''
# ── Concepts Agent: Explains topics ──────────────────────────────────────────

from pydantic import BaseModel

class ConceptRequest(BaseModel):
    user_id: str
    query: str
    context: Optional[str] = None
    level: str = "beginner"

@app.post("/explain")
async def explain_concept(req: ConceptRequest):
    """Explain a concept based on user query and level."""
    explanation = {
        "user_id": req.user_id,
        "query": req.query,
        "level": req.level,
        "explanation": f"Explanation for: {req.query}",
        "examples": [],
        "related_topics": [],
        "generated_at": datetime.now().isoformat(),
    }
    save_state(f"concepts:{req.user_id}:{hash(req.query)}", explanation)
    await publish_event("learning.progress", {
        "user_id": req.user_id,
        "event": "concept_viewed",
        "topic": req.query,
        "timestamp": datetime.now().isoformat(),
    })
    return explanation

@dapp.subscribe(pubsub_name="kafka", topic="learning.concepts")
async def on_concept_request(msg: Any) -> Response:
    """Handle concept explanation requests from pub/sub."""
    try:
        payload = json.loads(msg.body) if isinstance(msg.body, (str, bytes)) else msg.body
        req = ConceptRequest(**payload)
        await explain_concept(req)
        return Response(status_code=200)
    except Exception as e:
        logger.error("Failed to explain concept: %s", e)
        return Response(status_code=500)
''',

    "code-review": '''
# ── Code Review Agent: Analyzes code ─────────────────────────────────────────

from pydantic import BaseModel

class ReviewRequest(BaseModel):
    user_id: str
    query: str
    code: Optional[str] = None
    language: str = "python"
    context: Optional[str] = None

@app.post("/review")
async def review_code(req: ReviewRequest):
    """Review submitted code and provide feedback."""
    review_result = {
        "user_id": req.user_id,
        "language": req.language,
        "issues": [],
        "suggestions": [],
        "score": 0,
        "reviewed_at": datetime.now().isoformat(),
    }
    save_state(f"review:{req.user_id}:{hash(req.query)}", review_result)
    await publish_event("learning.progress", {
        "user_id": req.user_id,
        "event": "code_reviewed",
        "language": req.language,
        "timestamp": datetime.now().isoformat(),
    })
    return review_result

@dapp.subscribe(pubsub_name="kafka", topic="learning.review")
async def on_review_request(msg: Any) -> Response:
    """Handle code review requests from pub/sub."""
    try:
        payload = json.loads(msg.body) if isinstance(msg.body, (str, bytes)) else msg.body
        req = ReviewRequest(**payload)
        await review_code(req)
        return Response(status_code=200)
    except Exception as e:
        logger.error("Failed to review code: %s", e)
        return Response(status_code=500)
''',

    "debug": '''
# ── Debug Agent: Fixes errors ────────────────────────────────────────────────

from pydantic import BaseModel

class DebugRequest(BaseModel):
    user_id: str
    query: str
    error_message: Optional[str] = None
    code: Optional[str] = None
    language: str = "python"
    context: Optional[str] = None

@app.post("/debug")
async def debug_code(req: DebugRequest):
    """Debug code and suggest fixes for errors."""
    debug_result = {
        "user_id": req.user_id,
        "language": req.language,
        "error_message": req.error_message,
        "root_cause": "",
        "fix_suggestion": "",
        "fixed_code": "",
        "debugged_at": datetime.now().isoformat(),
    }
    save_state(f"debug:{req.user_id}:{hash(req.query)}", debug_result)
    await publish_event("learning.progress", {
        "user_id": req.user_id,
        "event": "code_debugged",
        "language": req.language,
        "timestamp": datetime.now().isoformat(),
    })
    return debug_result

@dapp.subscribe(pubsub_name="kafka", topic="learning.debug")
async def on_debug_request(msg: Any) -> Response:
    """Handle debug requests from pub/sub."""
    try:
        payload = json.loads(msg.body) if isinstance(msg.body, (str, bytes)) else msg.body
        req = DebugRequest(**payload)
        await debug_code(req)
        return Response(status_code=200)
    except Exception as e:
        logger.error("Failed to debug code: %s", e)
        return Response(status_code=500)
''',

    "exercise": '''
# ── Exercise Agent: Generates problems ───────────────────────────────────────

from pydantic import BaseModel

class ExerciseRequest(BaseModel):
    user_id: str
    query: str
    topic: Optional[str] = None
    difficulty: str = "medium"
    language: str = "python"
    context: Optional[str] = None

class SubmissionRequest(BaseModel):
    user_id: str
    exercise_id: str
    solution: str

@app.post("/generate")
async def generate_exercise(req: ExerciseRequest):
    """Generate a practice exercise for the user."""
    exercise = {
        "user_id": req.user_id,
        "exercise_id": f"ex-{hash(req.query)}",
        "topic": req.topic or req.query,
        "difficulty": req.difficulty,
        "language": req.language,
        "problem": f"Practice problem for: {req.query}",
        "hints": [],
        "test_cases": [],
        "generated_at": datetime.now().isoformat(),
    }
    save_state(f"exercise:{exercise['exercise_id']}", exercise)
    return exercise

@app.post("/submit")
async def submit_solution(req: SubmissionRequest):
    """Evaluate a submitted solution."""
    exercise = get_state(f"exercise:{req.exercise_id}")
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    result = {
        "user_id": req.user_id,
        "exercise_id": req.exercise_id,
        "passed": False,
        "feedback": "",
        "evaluated_at": datetime.now().isoformat(),
    }
    await publish_event("learning.progress", {
        "user_id": req.user_id,
        "event": "exercise_submitted",
        "exercise_id": req.exercise_id,
        "passed": result["passed"],
        "timestamp": datetime.now().isoformat(),
    })
    return result

@dapp.subscribe(pubsub_name="kafka", topic="learning.exercise")
async def on_exercise_request(msg: Any) -> Response:
    """Handle exercise generation requests from pub/sub."""
    try:
        payload = json.loads(msg.body) if isinstance(msg.body, (str, bytes)) else msg.body
        req = ExerciseRequest(**payload)
        await generate_exercise(req)
        return Response(status_code=200)
    except Exception as e:
        logger.error("Failed to generate exercise: %s", e)
        return Response(status_code=500)
''',

    "progress": '''
# ── Progress Agent: Tracks mastery ───────────────────────────────────────────

from pydantic import BaseModel

class ProgressEvent(BaseModel):
    user_id: str
    event: str
    topic: Optional[str] = None
    language: Optional[str] = None
    exercise_id: Optional[str] = None
    passed: Optional[bool] = None
    timestamp: Optional[str] = None

@app.get("/progress/{user_id}")
async def get_progress(user_id: str):
    """Get learning progress for a user."""
    progress = get_state(f"progress:{user_id}")
    if not progress:
        progress = {
            "user_id": user_id,
            "topics_viewed": [],
            "exercises_completed": 0,
            "exercises_passed": 0,
            "reviews_done": 0,
            "debug_sessions": 0,
            "mastery_scores": {},
            "last_active": None,
        }
    return progress

@app.post("/progress/{user_id}/reset")
async def reset_progress(user_id: str):
    """Reset progress for a user."""
    delete_state(f"progress:{user_id}")
    return {"status": "reset", "user_id": user_id}

@dapp.subscribe(pubsub_name="kafka", topic="learning.progress")
async def on_progress_event(msg: Any) -> Response:
    """Track learning progress events."""
    try:
        payload = json.loads(msg.body) if isinstance(msg.body, (str, bytes)) else msg.body
        event = ProgressEvent(**payload)

        progress = get_state(f"progress:{event.user_id}") or {
            "user_id": event.user_id,
            "topics_viewed": [],
            "exercises_completed": 0,
            "exercises_passed": 0,
            "reviews_done": 0,
            "debug_sessions": 0,
            "mastery_scores": {},
            "last_active": None,
        }

        progress["last_active"] = event.timestamp or datetime.now().isoformat()

        if event.event == "concept_viewed" and event.topic:
            if event.topic not in progress["topics_viewed"]:
                progress["topics_viewed"].append(event.topic)
        elif event.event == "code_reviewed":
            progress["reviews_done"] += 1
        elif event.event == "code_debugged":
            progress["debug_sessions"] += 1
        elif event.event == "exercise_submitted":
            progress["exercises_completed"] += 1
            if event.passed:
                progress["exercises_passed"] += 1

        save_state(f"progress:{event.user_id}", progress)
        logger.info("Updated progress for user %s: %s", event.user_id, event.event)
        return Response(status_code=200)
    except Exception as e:
        logger.error("Failed to update progress: %s", e)
        return Response(status_code=500)
''',
}

# ── Dockerfile Template ──────────────────────────────────────────────────────

DOCKERFILE_TEMPLATE = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

# ── Requirements Template ────────────────────────────────────────────────────

REQUIREMENTS_TEMPLATE = '''fastapi==0.109.0
uvicorn[standard]==0.27.0
python-dapr==1.13.0
dapr-ext-fastapi==1.13.0
kafka-python==2.0.2
psycopg2-binary==2.9.9
pydantic==2.5.3
httpx==0.26.0
'''

# ── Kubernetes Manifest Template ─────────────────────────────────────────────

K8S_MANIFEST_TEMPLATE = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  labels:
    app: {service_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "{service_name}"
        dapr.io/app-port: "8000"
        dapr.io/config: "learnflow-config"
        dapr.io/log-level: "info"
        dapr.io/sidecar-cpu-request: "100m"
        dapr.io/sidecar-memory-request: "128Mi"
    spec:
      containers:
        - name: {service_name}
          image: {service_name}:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8000
          env:
            - name: APP_PORT
              value: "8000"
            - name: STATE_STORE
              value: "postgres"
            - name: PUBSUB_NAME
              value: "kafka"
            - name: LOG_LEVEL
              value: "INFO"
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 10
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: {service_name}-svc
  labels:
    app: {service_name}
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8000
      protocol: TCP
  selector:
    app: {service_name}
'''
