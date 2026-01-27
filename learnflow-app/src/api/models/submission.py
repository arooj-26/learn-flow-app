"""Code submission and execution result models."""
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.api.models.base import Base, UUIDMixin


class CodeSubmission(Base, UUIDMixin):
    __tablename__ = "code_submissions"

    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    code = Column(Text, nullable=False)
    result = Column(Text)
    language = Column(String(50), default="python")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    student = relationship("User", back_populates="submissions")
    topic = relationship("Topic", back_populates="submissions")
    execution_result = relationship("ExecutionResult", back_populates="submission", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<CodeSubmission {self.id}>"


class ExecutionResult(Base, UUIDMixin):
    __tablename__ = "execution_results"

    submission_id = Column(UUID(as_uuid=True), ForeignKey("code_submissions.id", ondelete="CASCADE"), nullable=False)
    stdout = Column(Text)
    stderr = Column(Text)
    success = Column(Boolean, nullable=False, default=False)
    error_type = Column(Enum("syntax", "runtime", "logic", "timeout", "memory", name="error_type"))
    execution_time_ms = Column(Integer)
    memory_used_kb = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    submission = relationship("CodeSubmission", back_populates="execution_result")

    def __repr__(self) -> str:
        return f"<ExecutionResult success={self.success}>"
