"""Chat message model."""
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.api.models.base import Base, UUIDMixin


class ChatMessage(Base, UUIDMixin):
    __tablename__ = "chat_messages"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant', 'system')", name="ck_chat_role"),
    )

    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=True)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    agent_type = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    student = relationship("User", back_populates="chat_messages")

    def __repr__(self) -> str:
        return f"<ChatMessage {self.role}: {self.content[:50]}>"
