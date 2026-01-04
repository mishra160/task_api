from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_in: TaskCreate) -> Task:
    task = Task(
        title=task_in.title,
        description=task_in.description,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session, skip: int = 0, limit: int = 20) -> List[Task]:
    return (
        db.query(Task)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.is_completed is not None:
        task.is_completed = task_in.is_completed

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
