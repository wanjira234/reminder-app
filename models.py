from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from enum import Enum as PyEnum

class TaskStatus(str, PyEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    deadline = Column(DateTime)
    reminder_time = Column(DateTime)
    status = Column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED)
    week_number = Column(Integer, nullable=True)
    phase = Column(String, nullable=True)
    tools_resources = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    last_reminder = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks") 