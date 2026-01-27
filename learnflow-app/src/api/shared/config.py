"""Shared configuration for all agents."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://learnflow:learnflow@localhost:5432/learnflow")
    KAFKA_BOOTSTRAP: str = os.getenv("KAFKA_BOOTSTRAP", "learnflow-kafka-bootstrap:9092")
    DAPR_HTTP_PORT: str = os.getenv("DAPR_HTTP_PORT", "3500")
    DAPR_GRPC_PORT: str = os.getenv("DAPR_GRPC_PORT", "50001")
    PUBSUB_NAME: str = os.getenv("PUBSUB_NAME", "learnflow-pubsub")
    STATE_STORE_NAME: str = os.getenv("STATE_STORE_NAME", "learnflow-statestore")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SANDBOX_TIMEOUT: int = int(os.getenv("SANDBOX_TIMEOUT", "5"))
    SANDBOX_MEMORY_MB: int = int(os.getenv("SANDBOX_MEMORY_MB", "50"))


settings = Settings()

# Kafka topic names
TOPIC_LEARNING_SUBMITTED = "learning.submitted"
TOPIC_CODE_EXECUTED = "code.executed"
TOPIC_EXERCISE_STARTED = "exercise.started"
TOPIC_STRUGGLE_DETECTED = "struggle.detected"

# Agent service names (for Dapr service invocation)
TRIAGE_AGENT = "triage-agent"
CONCEPTS_AGENT = "concepts-agent"
CODE_REVIEW_AGENT = "code-review-agent"
DEBUG_AGENT = "debug-agent"
EXERCISE_AGENT = "exercise-agent"
PROGRESS_AGENT = "progress-agent"
