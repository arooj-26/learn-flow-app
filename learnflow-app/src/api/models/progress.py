"""Progress model."""
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.api.models.base import Base, UUIDMixin


class Progress(Base, UUIDMixin):
    __tablename__ = "progress"
    __table_args__ = (UniqueConstraint("student_id", "topic_id", name="uq_progress_student_topic"),)

    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    mastery = Column(Integer, nullable=False, default=0)
    exercises_done = Column(Integer, nullable=False, default=0)
    quiz_score = Column(Integer, nullable=False, default=0)
    code_quality = Column(Integer, nullable=False, default=0)
    streak = Column(Integer, nullable=False, default=0)
    last_activity = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    student = relationship("User", back_populates="progress_records")
    topic = relationship("Topic", back_populates="progress_records")

    @property
    def mastery_level(self) -> str:
        if self.mastery <= 40:
            return "beginner"
        elif self.mastery <= 70:
            return "learning"
        elif self.mastery <= 90:
            return "proficient"
        return "mastered"

    @property
    def mastery_color(self) -> str:
        colors = {"beginner": "red", "learning": "yellow", "proficient": "green", "mastered": "blue"}
        return colors[self.mastery_level]

    def calculate_mastery(self) -> int:
        """Mastery = 40% exercises + 30% quiz + 20% code_quality + 10% streak."""
        exercise_score = min(self.exercises_done * 10, 100)
        streak_score = min(self.streak * 10, 100)
        self.mastery = int(
            0.4 * exercise_score
            + 0.3 * self.quiz_score
            + 0.2 * self.code_quality
            + 0.1 * streak_score
        )
        self.mastery = max(0, min(100, self.mastery))
        return self.mastery

    def __repr__(self) -> str:
        return f"<Progress student={self.student_id} mastery={self.mastery}%>"
