"""Quiz and quiz result models."""
from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.api.models.base import Base, UUIDMixin


class Quiz(Base, UUIDMixin):
    __tablename__ = "quizzes"

    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    difficulty = Column(Enum("easy", "medium", "hard", name="difficulty_level"), nullable=False, default="medium")
    questions = Column(JSONB, nullable=False, default=list)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    topic = relationship("Topic", back_populates="quizzes")
    results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Quiz {self.title}>"


class QuizResult(Base, UUIDMixin):
    __tablename__ = "quiz_results"

    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    answers = Column(JSONB, nullable=False, default=dict)
    time_taken_seconds = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    student = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="results")

    def __repr__(self) -> str:
        return f"<QuizResult score={self.score}>"
