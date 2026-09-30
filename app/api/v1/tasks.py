"""
Tasks API router for task CRUD operations.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import UserModel
from app.models.task import TaskModel
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
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


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[TaskModel]:
    """
    List all tasks belonging to the currently authenticated user.
    """
    result = await db.execute(
        select(TaskModel).where(TaskModel.owner_id == current_user.id).order_by(TaskModel.created_at.desc())
    )
    tasks = result.scalars().all()
    return list(tasks)


@router.get("/{task_id}", response_model=TaskResponse)
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


@router.patch("/{task_id}", response_model=TaskResponse)
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


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a task by ID (ensuring ownership).
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
