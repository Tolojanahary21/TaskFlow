from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models.project import Project
from ..models.task import Task
from ..models.task_status import TaskStatus
from ..models.user import User
from ..crud.task_history import create_history
from ..schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskStatusChange,
    TaskAssign,
    TaskProgressUpdate
)

from ..crud.task import (
    get_task,
    get_tasks,
    create_task,
    update_task,
    delete_task
)


router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"]
)
# creer une tache
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project_task(
    project_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db)
):
    # Vérifier le projet
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

    # Vérifier que le status appartient au projet
    task_status = (
        db.query(TaskStatus)
        .filter(
            TaskStatus.id == data.status_id,
            TaskStatus.project_id == project_id
        )
        .first()
    )

    if not task_status:
        raise HTTPException(
            status_code=404,
            detail="Task status does not belong to this project"
        )

    # Vérifier l'assignee
    if data.assignee_id is not None:

        user = (
            db.query(User)
            .filter(User.id == data.assignee_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Vérifier que l'utilisateur est membre
        from ..models.project_member import ProjectMember

        member = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == data.assignee_id
            )
            .first()
        )

        if not member:
            raise HTTPException(
                status_code=400,
                detail="User is not a member of this project"
            )

    return create_task(
        db,
        project_id,
        data
    )
# ViewTask
@router.get(
    "",
    response_model=list[TaskResponse]
)
def list_project_tasks(
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

    return get_tasks(
        db,
        project_id
    )
# consulter une tache
@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_project_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db)
):
    task = get_task(
        db,
        project_id,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task
# Update task
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: int,
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()

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

    changes = []

    update_data = data.model_dump(exclude_unset=True)

    for field, new_value in update_data.items():
        old_value = getattr(task, field)

        if old_value != new_value:
            changes.append(
                (
                    field,
                    str(old_value) if old_value is not None else None,
                    str(new_value) if new_value is not None else None,
                )
            )

            setattr(task, field, new_value)

    if not changes:
        return task

    for field, old_value, new_value in changes:
        create_history(
            db=db,
            task_id=task.id,
            user_id=None,
            action="UPDATED",
            old_value=f"{field}: {old_value}",
            new_value=f"{field}: {new_value}",
        )

    db.commit()
    db.refresh(task)

    return task



def update_project_task(
    project_id: int,
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = get_task(
        db,
        project_id,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if data.status_id is not None:

        task_status = (
            db.query(TaskStatus)
            .filter(
                TaskStatus.id == data.status_id,
                TaskStatus.project_id == project_id
            )
            .first()
        )

        if not task_status:
            raise HTTPException(
                status_code=404,
                detail="Task status does not belong to this project"
            )

    if data.assignee_id is not None:

        user = (
            db.query(User)
            .filter(User.id == data.assignee_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        from ..models.project_member import ProjectMember

        member = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == data.assignee_id
            )
            .first()
        )

        if not member:
            raise HTTPException(
                status_code=400,
                detail="User is not a member of this project"
            )

    return update_task(
        db,
        task,
        data
    )
# delete task
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_project_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db)
):
    task = get_task(
        db,
        project_id,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    delete_task(
        db,
        task
    )

    return None
# update status
@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse
)
def change_task_status(
    project_id: int,
    task_id: int,
    data: TaskStatusChange,
    db: Session = Depends(get_db)
):
    task = get_task(
        db,
        project_id,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task_status = (
        db.query(TaskStatus)
        .filter(
            TaskStatus.id == data.status_id,
            TaskStatus.project_id == project_id
        )
        .first()
    )

    if not task_status:
        raise HTTPException(
            status_code=404,
            detail="Task status does not belong to this project"
        )
    
    old_status_id = task.status_id
    task.status_id = data.status_id
    create_history(
    db=db,
    task_id=task.id,
    user_id=None,
    action="STATUS_CHANGED",
    old_value=str(old_status_id),
    new_value=str(data.status_id),
)

    db.commit()
    db.refresh(task)

    return task
# Assigner task
@router.patch(
    "/{task_id}/assign",
    response_model=TaskResponse
)
def assign_task(
    project_id: int,
    task_id: int,
    data: TaskAssign,
    db: Session = Depends(get_db)
):
    task = get_task(
        db,
        project_id,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    user = (
        db.query(User)
        .filter(User.id == data.assignee_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    from ..models.project_member import ProjectMember

    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == data.assignee_id
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=400,
            detail="User is not a member of this project"
        )
    
    old_assignee_id = task.assignee_id
    task.assignee_id = data.assignee_id
    create_history(
    db=db,
    task_id=task.id,
    user_id=None,
    action="ASSIGNED",
    old_value=str(old_assignee_id) if old_assignee_id else None,
    new_value=str(data.assignee_id),
)

    db.commit()
    db.refresh(task)

    return task
# Update Progress
@router.patch(
    "/{task_id}/progress",
    response_model=TaskResponse
)
def update_task_progress(
    project_id: int,
    task_id: int,
    data: TaskProgressUpdate,
    db: Session = Depends(get_db)
):
    task = get_task(
        db,
        project_id,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    old_progress = task.progress
    task.progress = data.progress
    create_history(
    db=db,
    task_id=task.id,
    user_id=None,
    action="PROGRESS_CHANGED",
    old_value=str(old_progress),
    new_value=str(data.progress),
)

    db.commit()
    db.refresh(task)

    return task
# task completed 
@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse
)
def complete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db)
):
    task = get_task(
        db,
        project_id,
        task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    old_progress = task.progress
    task.progress = 100
    task.completed_at = datetime.now(timezone.utc)
    create_history(
    db=db,
    task_id=task.id,
    user_id=None,
    action="COMPLETED",
    old_value=str(old_progress),
    new_value="100",
)

    db.commit()
    db.refresh(task)

    return task