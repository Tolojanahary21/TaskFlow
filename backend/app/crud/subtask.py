from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..models.subtask import Subtask


def get_subtask(
    db: Session,
    task_id: int,
    subtask_id: int
):
    return (
        db.query(Subtask)
        .filter(
            Subtask.id == subtask_id,
            Subtask.task_id == task_id
        )
        .first()
    )


def get_subtasks(
    db: Session,
    task_id: int
):
    return (
        db.query(Subtask)
        .filter(
            Subtask.task_id == task_id
        )
        .order_by(
            Subtask.position.asc()
        )
        .all()
    )


def create_subtask(
    db: Session,
    task_id: int,
    data
):
    # Si aucune position utile n'est fournie,
    # on place la sous-tâche à la fin.
    if data.position == 0:
        last_subtask = (
            db.query(Subtask)
            .filter(Subtask.task_id == task_id)
            .order_by(Subtask.position.desc())
            .first()
        )

        if last_subtask:
            position = last_subtask.position + 1
        else:
            position = 0
    else:
        position = data.position

    subtask = Subtask(
        task_id=task_id,
        title=data.title,
        description=data.description,
        is_completed=False,
        position=position,
        completed_at=None
    )

    db.add(subtask)
    db.commit()
    db.refresh(subtask)

    return subtask


def update_subtask(
    db: Session,
    subtask: Subtask,
    data
):
    values = data.model_dump(
        exclude_unset=True
    )

    if "is_completed" in values:

        is_completed = values["is_completed"]

        if is_completed:
            subtask.is_completed = True
            subtask.completed_at = datetime.now(timezone.utc)

        else:
            subtask.is_completed = False
            subtask.completed_at = None

        values.pop("is_completed")

    for field, value in values.items():
        setattr(subtask, field, value)

    db.commit()
    db.refresh(subtask)

    return subtask


def complete_subtask(
    db: Session,
    subtask: Subtask
):
    subtask.is_completed = True
    subtask.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(subtask)

    return subtask


def reopen_subtask(
    db: Session,
    subtask: Subtask
):
    subtask.is_completed = False
    subtask.completed_at = None

    db.commit()
    db.refresh(subtask)

    return subtask


def reorder_subtasks(
    db: Session,
    task_id: int,
    subtask_ids: list[int]
):
    subtasks = (
        db.query(Subtask)
        .filter(
            Subtask.task_id == task_id
        )
        .all()
    )

    existing_ids = {subtask.id for subtask in subtasks}
    requested_ids = set(subtask_ids)

    if existing_ids != requested_ids:
        raise ValueError(
            "La liste des sous-tâches est invalide."
        )

    for position, subtask_id in enumerate(subtask_ids):

        subtask = next(
            subtask
            for subtask in subtasks
            if subtask.id == subtask_id
        )

        subtask.position = position

    db.commit()

    return get_subtasks(
        db=db,
        task_id=task_id
    )


def delete_subtask(
    db: Session,
    subtask: Subtask
):
    db.delete(subtask)
    db.commit()