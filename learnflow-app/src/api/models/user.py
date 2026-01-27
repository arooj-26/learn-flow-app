"""User model."""
from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.api.models.base import Base, UUIDMixin, TimestampMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("student", "teacher", name="user_role"), nullable=False, default="student")
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    enrolled_class = relationship("Class", back_populates="students", foreign_keys=[class_id])
    taught_classes = relationship("Class", back_populates="teacher", foreign_keys="Class.teacher_id")
    submissions = relationship("CodeSubmission", back_populates="student", cascade="all, delete-orphan")
    progress_records = relationship("Progress", back_populates="student", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="student", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="student", cascade="all, delete-orphan")
    struggle_events = relationship("StruggleEvent", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.name} ({self.role})>"
