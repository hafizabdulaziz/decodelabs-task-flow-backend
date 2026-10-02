"""
Pydantic v2 schemas for Task entity validation, serialization, and filtering.
"""

import enum
from datetime import datetime
from typing import Any
from typing_extensions import Annotated
from pydantic import BaseModel, Field, BeforeValidator
from app.models.task import TaskPriority, TaskStatus


class TaskSortField(str, enum.Enum):
    """
    Allowed task sorting fields.
    """
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    DUE_DATE = "due_date"
    TITLE = "title"


def parse_task_status(v: Any) -> TaskStatus:
    if isinstance(v, TaskStatus):
        return v
    if isinstance(v, str):
        v_lower = v.strip().lower().replace(" ", "_").replace("-", "_")
        mapping = {
            "pending": TaskStatus.PENDING,
            "in_progress": TaskStatus.IN_PROGRESS,
            "inprogress": TaskStatus.IN_PROGRESS,
            "completed": TaskStatus.COMPLETED,
            "complete": TaskStatus.COMPLETED,
        }
        if v_lower in mapping:
            return mapping[v_lower]
    return v


def parse_task_priority(v: Any) -> TaskPriority:
    if isinstance(v, TaskPriority):
        return v
    if isinstance(v, str):
        v_lower = v.strip().lower()
        mapping = {
            "low": TaskPriority.LOW,
            "medium": TaskPriority.MEDIUM,
            "high": TaskPriority.HIGH,
        }
        if v_lower in mapping:
            return mapping[v_lower]
    return v


NormTaskStatus = Annotated[TaskStatus, BeforeValidator(parse_task_status)]
NormTaskPriority = Annotated[TaskPriority, BeforeValidator(parse_task_priority)]


class TaskBase(BaseModel):
    """
    Base task schema with common fields.
    """
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    status: NormTaskStatus = TaskStatus.PENDING
    priority: NormTaskPriority = TaskPriority.MEDIUM
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
    status: NormTaskStatus | None = None
    priority: NormTaskPriority | None = None
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
