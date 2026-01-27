"""Triage Agent - Routes incoming queries to the appropriate specialist agent.

Routing rules:
- "error" keywords → Debug Agent
- "how does X work" patterns → Concepts Agent
- "fix code" / "review" patterns → Code Review Agent
- Default → Concepts Agent
"""
import logging
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.api.shared.config import (
    CONCEPTS_AGENT,
    CODE_REVIEW_AGENT,
    DEBUG_AGENT,
)
from src.api.shared.dapr_client import invoke_agent
from src.api.shared.schemas import TriageRequest, TriageResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("triage-agent")

# Routing patterns
ERROR_PATTERNS = re.compile(
    r"\b(error|exception|traceback|bug|crash|fail|broken|not working|wrong output)\b",
    re.IGNORECASE,
)
REVIEW_PATTERNS = re.compile(
    r"\b(fix|review|improve|refactor|check my code|code quality|pep\s?8|style)\b",
    re.IGNORECASE,
)
CONCEPT_PATTERNS = re.compile(
    r"\b(how does|what is|explain|teach|learn|understand|concept|example|show me|tutorial)\b",
    re.IGNORECASE,
)
STUCK_PATTERNS = re.compile(
    r"\b(i'?m stuck|help me|confused|don'?t understand|lost|no idea)\b",
    re.IGNORECASE,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Triage Agent starting")
    yield
    logger.info("Triage Agent shutting down")


app = FastAPI(
    title="LearnFlow Triage Agent",
    version="1.0.0",
    lifespan=lifespan,
)


def classify_query(message: str, has_code: bool) -> str:
    """Determine which agent should handle the query."""
    msg = message.lower().strip()

    # If they have code and mention errors -> debug
    if has_code and ERROR_PATTERNS.search(msg):
        return "debug"

    # If they mention fixing or reviewing code -> code review
    if has_code and REVIEW_PATTERNS.search(msg):
        return "code_review"

    # If they're asking about concepts -> concepts
    if CONCEPT_PATTERNS.search(msg):
        return "concepts"

    # If they say they're stuck -> debug (to help them get unstuck)
    if STUCK_PATTERNS.search(msg):
        return "debug" if has_code else "concepts"

    # If they provide code with no specific ask -> code review
    if has_code:
        return "code_review"

    # Default -> concepts
    return "concepts"


AGENT_MAP = {
    "debug": (DEBUG_AGENT, "analyze"),
    "code_review": (CODE_REVIEW_AGENT, "review"),
    "concepts": (CONCEPTS_AGENT, "explain"),
}


@app.post("/triage", response_model=TriageResponse)
async def triage(request: TriageRequest) -> TriageResponse:
    """Route a student query to the appropriate specialist agent."""
    agent_key = classify_query(request.message, bool(request.code))
    agent_name, method = AGENT_MAP[agent_key]

    logger.info(
        "Routing student %s to %s (message: %s...)",
        request.student_id,
        agent_name,
        request.message[:50],
    )

    try:
        payload = {
            "student_id": str(request.student_id),
            "message": request.message,
        }
        if request.code:
            payload["code"] = request.code
        if request.topic_id:
            payload["topic_id"] = str(request.topic_id)

        result = await invoke_agent(agent_name, method, payload)
        return TriageResponse(agent=agent_name, response=result)

    except Exception as e:
        logger.error("Failed to invoke %s: %s", agent_name, str(e))
        raise HTTPException(status_code=502, detail=f"Agent {agent_name} unavailable")


class HealthResponse(BaseModel):
    status: str
    agent: str


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", agent="triage-agent")


@app.get("/dapr/subscribe")
async def subscribe():
    """Dapr subscription configuration."""
    return []
