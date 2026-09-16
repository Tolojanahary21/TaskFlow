from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.project import Project
from ..models.task import Task
from ..schemas.task_history import TaskHistoryResponse
from ..crud.task_history import get_task_history


router = APIRouter(
    prefix="/projects/{project_id}/tasks/{task_id}/history",
    tags=["Task History"]
)


@router.get(
    "",
    response_model=list[TaskHistoryResponse]
)
def list_task_history(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.project_id == project_id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return get_task_history(db, task_id)