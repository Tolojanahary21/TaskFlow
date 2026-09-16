from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.project import Project
from ..schemas.task_status import (
    TaskStatusCreate,
    TaskStatusUpdate,
    TaskStatusResponse,
    TaskStatusReorder
)
from ..crud.task_status import (
    get_task_status,
    get_task_statuses,
    create_task_status,
    update_task_status,
    delete_task_status
)
from ..models.task_status import TaskStatus


router = APIRouter(
    prefix="/projects/{project_id}/statuses",
    tags=["Task Statuses"]
)
# ajouter un status
@router.post(
    "",
    response_model=TaskStatusResponse,
    status_code=status.HTTP_201_CREATED
)
def create_status(
    project_id: int,
    data: TaskStatusCreate,
    db: Session = Depends(get_db)
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

    existing_status = (
        db.query(TaskStatus)
        .filter(
            TaskStatus.project_id == project_id,
            TaskStatus.name == data.name
        )
        .first()
    )

    if existing_status:
        raise HTTPException(
            status_code=409,
            detail="A status with this name already exists in this project"
        )

    return create_task_status(
        db,
        project_id,
        data.name,
        data.position,
        data.color
    )
# consulter les status
@router.get(
    "",
    response_model=list[TaskStatusResponse]
)
def list_statuses(
    project_id: int,
    db: Session = Depends(get_db)
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

    return get_task_statuses(
        db,
        project_id
    )
# update status
@router.patch(
    "/{status_id}",
    response_model=TaskStatusResponse
)
def update_status(
    project_id: int,
    status_id: int,
    data: TaskStatusUpdate,
    db: Session = Depends(get_db)
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

    task_status = get_task_status(
        db,
        project_id,
        status_id
    )

    if not task_status:
        raise HTTPException(
            status_code=404,
            detail="Task status not found"
        )

    if data.name is not None:
        existing_status = (
            db.query(TaskStatus)
            .filter(
                TaskStatus.project_id == project_id,
                TaskStatus.name == data.name,
                TaskStatus.id != status_id
            )
            .first()
        )

        if existing_status:
            raise HTTPException(
                status_code=409,
                detail="A status with this name already exists in this project"
            )

    return update_task_status(
        db,
        task_status,
        data.name,
        data.position,
        data.color
    )
# reordonnance des status
@router.patch(
    "/{status_id}/reorder",
    response_model=TaskStatusResponse
)
def reorder_status(
    project_id: int,
    status_id: int,
    data: TaskStatusReorder,
    db: Session = Depends(get_db)
):
    task_status = get_task_status(
        db,
        project_id,
        status_id
    )

    if not task_status:
        raise HTTPException(
            status_code=404,
            detail="Task status not found"
        )

    task_status.position = data.position

    db.commit()
    db.refresh(task_status)

    return task_status