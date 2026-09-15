from sqlalchemy.orm import Session

from ..models.task_status import TaskStatus


def get_task_status(
    db: Session,
    project_id: int,
    status_id: int
):
    return (
        db.query(TaskStatus)
        .filter(
            TaskStatus.id == status_id,
            TaskStatus.project_id == project_id
        )
        .first()
    )


def get_task_statuses(
    db: Session,
    project_id: int
):
    return (
        db.query(TaskStatus)
        .filter(TaskStatus.project_id == project_id)
        .order_by(TaskStatus.position.asc())
        .all()
    )


def create_task_status(
    db: Session,
    project_id: int,
    name: str,
    position: int,
    color: str | None
):
    task_status = TaskStatus(
        project_id=project_id,
        name=name,
        position=position,
        color=color
    )

    db.add(task_status)
    db.commit()
    db.refresh(task_status)

    return task_status


def update_task_status(
    db: Session,
    task_status: TaskStatus,
    name: str | None = None,
    position: int | None = None,
    color: str | None = None
):
    if name is not None:
        task_status.name = name

    if position is not None:
        task_status.position = position

    if color is not None:
        task_status.color = color

    db.commit()
    db.refresh(task_status)

    return task_status


def delete_task_status(
    db: Session,
    task_status: TaskStatus
):
    db.delete(task_status)
    db.commit()