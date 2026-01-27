"""Progress Agent - Calculate mastery, detect struggling topics, emit struggle events.

Mastery formula: 40% exercises + 30% quiz + 20% code_quality + 10% streak
Mastery levels: 0-40% Beginner(Red), 41-70% Learning(Yellow), 71-90% Proficient(Green), 91-100% Mastered(Blue)
Struggle detection: same error 3+, stuck >10min, quiz <50%, "I'm stuck", 5+ failed executions
"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import func, select

from src.api.shared.config import TOPIC_STRUGGLE_DETECTED, settings
from src.api.shared.dapr_client import publish_event
from src.api.shared.database import get_session
from src.api.shared.schemas import (
    MasteryLevel,
    ProgressRequest,
    ProgressResponse,
    TopicProgress,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("progress-agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Progress Agent starting")
    yield
    logger.info("Progress Agent shutting down")


app = FastAPI(title="LearnFlow Progress Agent", version="1.0.0", lifespan=lifespan)


def calculate_mastery(exercises_done: int, quiz_score: int, code_quality: int, streak: int) -> int:
    """Mastery = 40% exercises + 30% quiz + 20% code_quality + 10% streak."""
    exercise_score = min(exercises_done * 10, 100)  # Cap at 100
    streak_score = min(streak * 10, 100)
    mastery = int(
        0.4 * exercise_score
        + 0.3 * quiz_score
        + 0.2 * code_quality
        + 0.1 * streak_score
    )
    return max(0, min(100, mastery))


def get_mastery_level(mastery: int) -> MasteryLevel:
    """Map mastery % to level."""
    if mastery <= 40:
        return MasteryLevel.BEGINNER
    elif mastery <= 70:
        return MasteryLevel.LEARNING
    elif mastery <= 90:
        return MasteryLevel.PROFICIENT
    return MasteryLevel.MASTERED


@app.post("/calculate", response_model=ProgressResponse)
async def calculate_progress(request: ProgressRequest) -> ProgressResponse:
    """Calculate mastery for all topics (or a specific topic) for a student."""
    logger.info("Calculating progress for student %s", request.student_id)

    from src.api.models.progress import Progress
    from src.api.models.topic import Topic

    topics_progress: list[TopicProgress] = []
    struggling: list[TopicProgress] = []

    async with get_session() as session:
        if request.topic_id:
            query = select(Progress).where(
                Progress.student_id == request.student_id,
                Progress.topic_id == request.topic_id,
            )
        else:
            query = select(Progress).where(Progress.student_id == request.student_id)

        result = await session.execute(query)
        records = result.scalars().all()

        for record in records:
            # Recalculate mastery
            mastery = calculate_mastery(
                record.exercises_done,
                record.quiz_score,
                record.code_quality,
                record.streak,
            )
            level = get_mastery_level(mastery)

            # Get topic name
            topic_result = await session.execute(
                select(Topic.name).where(Topic.id == record.topic_id)
            )
            topic_name = topic_result.scalar_one_or_none() or "Unknown"

            tp = TopicProgress(
                topic_id=record.topic_id,
                topic_name=topic_name,
                mastery=mastery,
                level=level,
                exercises_done=record.exercises_done,
                quiz_score=record.quiz_score,
                code_quality=record.code_quality,
                streak=record.streak,
            )
            topics_progress.append(tp)

            # Struggling: mastery < 40%
            if mastery < 40:
                struggling.append(tp)

                # Emit struggle event
                await publish_event(TOPIC_STRUGGLE_DETECTED, {
                    "student_id": str(request.student_id),
                    "topic_id": str(record.topic_id),
                    "reason": f"Low mastery ({mastery}%) on {topic_name}",
                })

    overall = 0
    if topics_progress:
        overall = int(sum(t.mastery for t in topics_progress) / len(topics_progress))

    return ProgressResponse(
        student_id=request.student_id,
        overall_mastery=overall,
        topics=topics_progress,
        struggling_topics=struggling,
    )


class UpdateProgressRequest(BaseModel):
    student_id: str
    topic_id: str
    exercises_done: int | None = None
    quiz_score: int | None = None
    code_quality: int | None = None
    streak: int | None = None


class UpdateProgressResponse(BaseModel):
    mastery: int
    level: str
    previous_mastery: int


@app.post("/update", response_model=UpdateProgressResponse)
async def update_progress(request: UpdateProgressRequest) -> UpdateProgressResponse:
    """Update progress metrics and recalculate mastery."""
    logger.info("Updating progress for student %s on topic %s", request.student_id, request.topic_id)

    from src.api.models.progress import Progress

    async with get_session() as session:
        result = await session.execute(
            select(Progress).where(
                Progress.student_id == request.student_id,
                Progress.topic_id == request.topic_id,
            )
        )
        record = result.scalar_one_or_none()

        if not record:
            record = Progress(
                student_id=request.student_id,
                topic_id=request.topic_id,
                exercises_done=0,
                quiz_score=0,
                code_quality=0,
                streak=0,
                mastery=0,
            )
            session.add(record)

        previous_mastery = record.mastery

        if request.exercises_done is not None:
            record.exercises_done = request.exercises_done
        if request.quiz_score is not None:
            record.quiz_score = request.quiz_score
        if request.code_quality is not None:
            record.code_quality = request.code_quality
        if request.streak is not None:
            record.streak = request.streak

        record.mastery = calculate_mastery(
            record.exercises_done,
            record.quiz_score,
            record.code_quality,
            record.streak,
        )
        record.last_activity = datetime.now(timezone.utc)

        await session.flush()

    level = get_mastery_level(record.mastery)
    return UpdateProgressResponse(
        mastery=record.mastery,
        level=level.value,
        previous_mastery=previous_mastery,
    )


class StruggleCheckRequest(BaseModel):
    student_id: str
    topic_id: str
    error_count: int = 0
    minutes_stuck: int = 0
    failed_executions: int = 0
    quiz_score: int | None = None
    message: str | None = None


class StruggleCheckResponse(BaseModel):
    struggling: bool
    reasons: list[str]


@app.post("/check-struggle", response_model=StruggleCheckResponse)
async def check_struggle(request: StruggleCheckRequest) -> StruggleCheckResponse:
    """Check if a student is struggling based on multiple signals."""
    reasons: list[str] = []

    # Same error 3+ times
    if request.error_count >= 3:
        reasons.append(f"Same error repeated {request.error_count} times")

    # Stuck >10 minutes
    if request.minutes_stuck > 10:
        reasons.append(f"Stuck for {request.minutes_stuck} minutes")

    # Quiz score <50%
    if request.quiz_score is not None and request.quiz_score < 50:
        reasons.append(f"Quiz score below 50% ({request.quiz_score}%)")

    # Says "I'm stuck"
    if request.message and any(phrase in request.message.lower() for phrase in ["i'm stuck", "im stuck", "stuck", "help me", "confused", "don't understand"]):
        reasons.append("Student expressed difficulty")

    # 5+ failed executions
    if request.failed_executions >= 5:
        reasons.append(f"{request.failed_executions} failed code executions")

    struggling = len(reasons) > 0

    if struggling:
        logger.warning("Struggle detected for student %s on topic %s: %s", request.student_id, request.topic_id, reasons)
        await publish_event(TOPIC_STRUGGLE_DETECTED, {
            "student_id": request.student_id,
            "topic_id": request.topic_id,
            "reason": "; ".join(reasons),
        })

    return StruggleCheckResponse(struggling=struggling, reasons=reasons)


class HealthResponse(BaseModel):
    status: str
    agent: str


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", agent="progress-agent")


@app.get("/dapr/subscribe")
async def subscribe():
    """Dapr subscriptions - listen for code execution and learning events."""
    return [
        {
            "pubsubname": settings.PUBSUB_NAME,
            "topic": "code.executed",
            "route": "/events/code-executed",
        },
        {
            "pubsubname": settings.PUBSUB_NAME,
            "topic": "learning.submitted",
            "route": "/events/learning-submitted",
        },
    ]


@app.post("/events/code-executed")
async def handle_code_executed(event: dict):
    """Handle code execution results from Kafka."""
    data = event.get("data", {})
    logger.info("Code executed event: submission=%s success=%s", data.get("submission_id"), data.get("success"))
    return {"status": "ok"}


@app.post("/events/learning-submitted")
async def handle_learning_submitted(event: dict):
    """Handle new learning submission events from Kafka."""
    data = event.get("data", {})
    logger.info("Learning submitted: student=%s topic=%s", data.get("student_id"), data.get("topic_id"))
    return {"status": "ok"}
