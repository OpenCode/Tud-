from typing import Optional
from datetime import datetime, UTC
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base


# ===============
# Database Models
# ===============

Base = declarative_base()

class TaskModel(Base):
    __tablename__ = "task"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))


# ===========
# APIs Models
# ===========


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
