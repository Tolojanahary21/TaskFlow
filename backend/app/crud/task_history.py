from sqlalchemy.orm import Session

from ..models.task_history import TaskHistory


def create_history(
    db: Session,
    task_id: int,
    user_id: int | None,
    action: str,
    old_value: str | None = None,
    new_value: str | None = None,
):
    history = TaskHistory(
        task_id=task_id,
        user_id=user_id,
        action=action,
        old_value=old_value,
        new_value=new_value,
    )

    db.add(history)

    return history

def get_task_history(db: Session, task_id: int):
    return (
        db.query(TaskHistory)
        .filter(TaskHistory.task_id == task_id)
        .order_by(TaskHistory.created_at.desc())
        .all()
    )