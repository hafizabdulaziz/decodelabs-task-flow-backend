"""
Tasks API router for task CRUD operations.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.db.session import get_db
from app.models.user import UserModel
from app.models.task import TaskModel, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskSortField
from app.schemas.error import ErrorResponse
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

STANDARD_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    422: {"model": ErrorResponse, "description": "Validation Error"},
    429: {"model": ErrorResponse, "description": "Rate Limit Exceeded"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": TaskResponse, "description": "Task successfully created"},
        **STANDARD_RESPONSES,
    },
    summary="Create Task",
    description="Create a new task owned by the currently authenticated user.",
)
async def create_task(
    task_in: TaskCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TaskModel:
    """
    Create a new task owned by the currently authenticated user.
    """
    new_task = TaskModel(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        priority=task_in.priority,
        due_date=task_in.due_date,
        owner_id=current_user.id,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get(
    "/",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": List[TaskResponse], "description": "List of tasks retrieved successfully"},
        **STANDARD_RESPONSES,
    },
    summary="List Tasks",
    description="List all tasks belonging to the currently authenticated user with pagination, filtering, search, and sorting.",
)
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    status_filter: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    q: str | None = None,
    sort_by: TaskSortField = TaskSortField.CREATED_AT,
    order: str = "desc",
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[TaskModel]:
    """
    List all tasks belonging to the currently authenticated user with pagination, filtering, case-insensitive search, and strict enum sorting.
    """
    query = select(TaskModel).where(TaskModel.owner_id == current_user.id)

    if status_filter is not None:
        query = query.where(TaskModel.status == status_filter)
    if priority is not None:
        query = query.where(TaskModel.priority == priority)
    if q is not None and q.strip():
        search_term = f"%{q.strip()}%"
        query = query.where(
            or_(
                TaskModel.title.ilike(search_term),
                TaskModel.description.ilike(search_term),
            )
        )

    # Strict Enum Sorting
    sort_column = getattr(TaskModel, sort_by.value, TaskModel.created_at)
    if order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    tasks = result.scalars().all()
    return list(tasks)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": TaskResponse, "description": "Task retrieved successfully"},
        **STANDARD_RESPONSES,
    },
    summary="Get Task by ID",
    description="Get a single task by ID ensuring user ownership.",
)
async def get_task(
    task_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TaskModel:
    """
    Get a single task by ID (ensuring ownership).
    """
    result = await db.execute(
        select(TaskModel).where(TaskModel.id == task_id, TaskModel.owner_id == current_user.id)
    )
    task = result.scalars().first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": TaskResponse, "description": "Task updated successfully"},
        **STANDARD_RESPONSES,
    },
    summary="Update Task",
    description="Update an existing task by ID ensuring user ownership.",
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TaskModel:
    """
    Update an existing task by ID (ensuring ownership).
    """
    result = await db.execute(
        select(TaskModel).where(TaskModel.id == task_id, TaskModel.owner_id == current_user.id)
    )
    task = result.scalars().first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Task successfully deleted (Empty Body)"},
        **STANDARD_RESPONSES,
    },
    summary="Delete Task",
    description="Delete a task by ID ensuring user ownership. Returns 204 No Content on success.",
)
async def delete_task(
    task_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a task by ID (ensuring ownership). Returns 204 No Content on success.
    """
    result = await db.execute(
        select(TaskModel).where(TaskModel.id == task_id, TaskModel.owner_id == current_user.id)
    )
    task = result.scalars().first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    await db.delete(task)
    await db.commit()
    return None
