"""API Gateway - Routes frontend requests to the correct agent service.

This runs when NOT using Dapr service invocation (local dev mode).
In Kubernetes with Dapr, the frontend calls agents directly via Dapr sidecar.
"""
import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gateway")

# Agent service URLs (local dev - Docker Compose)
AGENT_URLS = {
    "triage-agent": "http://localhost:8000",
    "concepts-agent": "http://localhost:8001",
    "code-review-agent": "http://localhost:8002",
    "debug-agent": "http://localhost:8003",
    "exercise-agent": "http://localhost:8004",
    "progress-agent": "http://localhost:8005",
    "code-sandbox": "http://localhost:8010",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("API Gateway starting")
    yield
    logger.info("API Gateway shutting down")


app = FastAPI(title="LearnFlow API Gateway", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.api_route("/{agent_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(agent_name: str, path: str, request: Request):
    """Proxy requests to the appropriate agent."""
    if agent_name not in AGENT_URLS:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {agent_name}")

    target_url = f"{AGENT_URLS[agent_name]}/{path}"
    body = await request.body()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                content=body,
                headers={"Content-Type": "application/json"},
            )
            return JSONResponse(status_code=response.status_code, content=response.json())
        except httpx.RequestError as e:
            logger.error("Proxy error for %s: %s", agent_name, str(e))
            raise HTTPException(status_code=502, detail=f"Agent {agent_name} unavailable")


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "gateway"}
