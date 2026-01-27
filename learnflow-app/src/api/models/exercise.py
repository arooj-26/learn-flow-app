"""Exercise model."""
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.api.models.base import Base, UUIDMixin


class Exercise(Base, UUIDMixin):
    __tablename__ = "exercises"

    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum("easy", "medium", "hard", name="difficulty_level"), nullable=False, default="medium")
    starter_code = Column(Text)
    test_cases = Column(JSONB, nullable=False, default=list)
    hints = Column(JSONB, default=list)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    topic = relationship("Topic", back_populates="exercises")

    def __repr__(self) -> str:
        return f"<Exercise {self.title}>"
