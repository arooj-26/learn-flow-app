"""Class (classroom) model."""
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.api.models.base import Base, UUIDMixin, TimestampMixin


class Class(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "classes"

    name = Column(String(255), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text)

    # Relationships
    teacher = relationship("User", back_populates="taught_classes", foreign_keys=[teacher_id])
    students = relationship("User", back_populates="enrolled_class", foreign_keys="User.class_id")
    modules = relationship("Module", back_populates="class_", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Class {self.name}>"
