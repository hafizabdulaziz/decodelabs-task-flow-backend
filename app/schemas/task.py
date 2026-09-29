"""
Pydantic v2 schemas for Task entity validation, serialization, and filtering.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from app.models.task import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    """
    Base task schema with common fields.
    """
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task (partial updates supported).
    """
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class TaskResponse(TaskBase):
    """
    Schema for serializing task responses.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
