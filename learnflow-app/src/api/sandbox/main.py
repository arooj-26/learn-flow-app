"""Code Sandbox FastAPI service - Secure Python code execution endpoint.

MCP-compatible code execution server.
Timeout: 5s, Memory: 50MB, No filesystem (except /tmp), No network, Stdlib only.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sandbox")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Code Sandbox starting (timeout=5s, memory=50MB)")
    yield
    logger.info("Code Sandbox shutting down")


app = FastAPI(
    title="LearnFlow Code Sandbox",
    version="1.0.0",
    description="Secure Python code execution sandbox for LearnFlow",
    lifespan=lifespan,
)


class ExecuteRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=10000, description="Python code to execute")
    timeout: int = Field(default=5, ge=1, le=10, description="Timeout in seconds")
    memory_mb: int = Field(default=50, ge=10, le=100, description="Memory limit in MB")


class ExecuteResponse(BaseModel):
    stdout: str
    stderr: str
    success: bool
    error_type: str | None = None
    execution_time_ms: int


@app.post("/execute", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest) -> ExecuteResponse:
    """Execute Python code in a sandboxed environment."""
    logger.info("Executing code (%d chars, timeout=%ds, memory=%dMB)",
                len(request.code), request.timeout, request.memory_mb)

    # Validate code doesn't contain obviously dangerous patterns
    dangerous = ["import os", "import subprocess", "import socket", "import shutil",
                 "__import__", "eval(", "exec(", "compile("]
    code_lower = request.code.lower()
    for pattern in dangerous:
        if pattern.lower() in code_lower:
            return ExecuteResponse(
                stdout="",
                stderr=f"SecurityError: '{pattern}' is not allowed in the sandbox",
                success=False,
                error_type="runtime",
                execution_time_ms=0,
            )

    try:
        from src.api.sandbox.executor import execute_sandboxed
        result = execute_sandboxed(request.code, request.timeout, request.memory_mb)
        return ExecuteResponse(**result)
    except Exception as e:
        logger.error("Sandbox execution error: %s", str(e))
        return ExecuteResponse(
            stdout="",
            stderr=f"InternalError: {str(e)}",
            success=False,
            error_type="runtime",
            execution_time_ms=0,
        )


class HealthResponse(BaseModel):
    status: str
    service: str


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", service="code-sandbox")
