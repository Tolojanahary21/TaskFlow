from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud.subtask import (
    complete_subtask,
    create_subtask,
    delete_subtask,
    get_subtask,
    get_subtasks,
    reopen_subtask,
    reorder_subtasks,
    update_subtask,
)
from ..database import get_db
from ..models.task import Task
from ..schemas.subtask import (
    SubtaskCreate,
    SubtaskResponse,
    SubtaskUpdate,
)


router = APIRouter(
    prefix="/tasks/{task_id}/subtasks",
    tags=["Subtasks"],
)


def verify_task(
    db: Session,
    task_id: int
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable."
        )

    return task


@router.post(
    "",
    response_model=SubtaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_subtask(
    task_id: int,
    data: SubtaskCreate,
    db: Session = Depends(get_db),
):
    verify_task(db, task_id)

    return create_subtask(
        db=db,
        task_id=task_id,
        data=data,
    )


@router.get(
    "",
    response_model=list[SubtaskResponse],
)
def list_subtasks(
    task_id: int,
    db: Session = Depends(get_db),
):
    verify_task(db, task_id)

    return get_subtasks(
        db=db,
        task_id=task_id,
    )


@router.patch(
    "/reorder",
    response_model=list[SubtaskResponse],
)
def reorder(
    task_id: int,
    subtask_ids: list[int],
    db: Session = Depends(get_db),
):
    verify_task(db, task_id)

    try:
        return reorder_subtasks(
            db=db,
            task_id=task_id,
            subtask_ids=subtask_ids,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{subtask_id}",
    response_model=SubtaskResponse,
)
def get_one_subtask(
    task_id: int,
    subtask_id: int,
    db: Session = Depends(get_db),
):
    verify_task(db, task_id)

    subtask = get_subtask(
        db=db,
        task_id=task_id,
        subtask_id=subtask_id,
    )

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sous-tâche introuvable."
        )

    return subtask


@router.put(
    "/{subtask_id}",
    response_model=SubtaskResponse,
)
def edit_subtask(
    task_id: int,
    subtask_id: int,
    data: SubtaskUpdate,
    db: Session = Depends(get_db),
):
    verify_task(db, task_id)

    subtask = get_subtask(
        db=db,
        task_id=task_id,
        subtask_id=subtask_id,
    )

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sous-tâche introuvable."
        )

    return update_subtask(
        db=db,
        subtask=subtask,
        data=data,
    )


@router.delete(
    "/{subtask_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_subtask(
    task_id: int,
    subtask_id: int,
    db: Session = Depends(get_db),
):
    verify_task(db, task_id)

    subtask = get_subtask(
        db=db,
        task_id=task_id,
        subtask_id=subtask_id,
    )

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sous-tâche introuvable."
        )

    delete_subtask(
        db=db,
        subtask=subtask,
    )

    return None


@router.patch(
    "/{subtask_id}/complete",
    response_model=SubtaskResponse,
)
def mark_subtask_complete(
    task_id: int,
    subtask_id: int,
    db: Session = Depends(get_db),
):
    verify_task(db, task_id)

    subtask = get_subtask(
        db=db,
        task_id=task_id,
        subtask_id=subtask_id,
    )

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sous-tâche introuvable."
        )

    return complete_subtask(
        db=db,
        subtask=subtask,
    )


@router.patch(
    "/{subtask_id}/reopen",
    response_model=SubtaskResponse,
)
def reopen_one_subtask(
    task_id: int,
    subtask_id: int,
    db: Session = Depends(get_db),
):
    verify_task(db, task_id)

    subtask = get_subtask(
        db=db,
        task_id=task_id,
        subtask_id=subtask_id,
    )

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sous-tâche introuvable."
        )

    return reopen_subtask(
        db=db,
        subtask=subtask,
    )