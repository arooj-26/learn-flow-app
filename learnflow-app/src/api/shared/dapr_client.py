"""Dapr HTTP client for service invocation and pub/sub."""
import logging
from typing import Any

import httpx

from src.api.shared.config import settings

logger = logging.getLogger(__name__)

DAPR_BASE_URL = f"http://localhost:{settings.DAPR_HTTP_PORT}/v1.0"


async def invoke_agent(agent_name: str, method: str, data: dict[str, Any]) -> dict[str, Any]:
    """Invoke another agent via Dapr service invocation."""
    url = f"{DAPR_BASE_URL}/invoke/{agent_name}/method/{method}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error("Agent invocation failed: %s %s -> %d", agent_name, method, e.response.status_code)
            raise
        except httpx.RequestError as e:
            logger.error("Agent invocation error: %s %s -> %s", agent_name, method, str(e))
            raise


async def publish_event(topic: str, data: dict[str, Any]) -> None:
    """Publish an event to a Kafka topic via Dapr pub/sub."""
    url = f"{DAPR_BASE_URL}/publish/{settings.PUBSUB_NAME}/{topic}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(url, json=data)
            response.raise_for_status()
            logger.info("Published event to %s", topic)
        except httpx.HTTPError as e:
            logger.error("Failed to publish to %s: %s", topic, str(e))
            raise


async def get_state(key: str) -> Any | None:
    """Get state from Dapr state store."""
    url = f"{DAPR_BASE_URL}/state/{settings.STATE_STORE_NAME}/{key}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        if response.status_code == 204:
            return None
        response.raise_for_status()
        return response.json()


async def save_state(key: str, value: Any) -> None:
    """Save state to Dapr state store."""
    url = f"{DAPR_BASE_URL}/state/{settings.STATE_STORE_NAME}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=[{"key": key, "value": value}])
        response.raise_for_status()
