from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
)

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED
)
def create_task_route(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(db, task_in)


@router.get(
    "/",
    response_model=List[TaskRead]
)
def list_tasks_route(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return get_tasks(db, skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=TaskRead
)
def get_task_route(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.put(
    "/{task_id}",
    response_model=TaskRead
)
def update_task_route(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return update_task(db, task, task_in)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task_route(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    delete_task(db, task)
    return None
