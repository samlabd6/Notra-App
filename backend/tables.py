from sqlalchemy import (
    Column, Integer, String, Text,
    DateTime, Boolean, ForeignKey, func
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    notes = relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)
    context = Column(Text)

    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    is_archived = Column(Boolean, default=False)

    user = relationship("User", back_populates="notes")