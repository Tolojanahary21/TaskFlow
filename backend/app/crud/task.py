from datetime import datetime

from sqlalchemy.orm import Session

from ..models.task import Task


def get_task(
    db: Session,
    project_id: int,
    task_id: int
):
    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.project_id == project_id
        )
        .first()
    )


def get_tasks(
    db: Session,
    project_id: int
):
    return (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .order_by(Task.created_at.desc())
        .all()
    )


def create_task(
    db: Session,
    project_id: int,
    data
):
    task = Task(
        project_id=project_id,
        status_id=data.status_id,
        assignee_id=data.assignee_id,
        title=data.title,
        description=data.description,
        priority=data.priority.value,
        complexity=data.complexity.value,
        task_type=data.task_type.value,
        estimated_duration=data.estimated_duration,
        predicted_duration=data.predicted_duration,
        actual_duration=data.actual_duration,
        progress=data.progress,
        start_date=data.start_date,
        due_date=data.due_date
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task(
    db: Session,
    task: Task,
    data
):
    values = data.model_dump(
        exclude_unset=True
    )

    for field, value in values.items():

        if hasattr(value, "value"):
            value = value.value

        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task
):
    db.delete(task)
    db.commit()