"""Struggle event model."""
from datetime import datetime, timezone

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.api.models.base import Base, UUIDMixin


class StruggleEvent(Base, UUIDMixin):
    __tablename__ = "struggle_events"

    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String(255), nullable=False)
    details = Column(JSONB)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    student = relationship("User", back_populates="struggle_events")

    def __repr__(self) -> str:
        return f"<StruggleEvent {self.reason}>"
