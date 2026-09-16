from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud.task_dependency import (
    create_dependency,
    delete_dependency,
    get_dependencies,
    get_dependency,
)
from ..database import get_db
from ..schemas.task_dependency import (
    TaskDependencyCreate,
    TaskDependencyResponse,
)


router = APIRouter(
    prefix="/projects/{project_id}/task-dependencies",
    tags=["Task Dependencies"],
)


@router.post(
    "",
    response_model=TaskDependencyResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_dependency(
    project_id: int,
    data: TaskDependencyCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_dependency(
            db=db,
            project_id=project_id,
            data=data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[TaskDependencyResponse],
)
def list_dependencies(
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_dependencies(
        db=db,
        project_id=project_id,
    )


@router.delete(
    "/{dependency_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_dependency(
    project_id: int,
    dependency_id: int,
    db: Session = Depends(get_db),
):
    dependency = get_dependency(
        db=db,
        dependency_id=dependency_id,
    )

    if not dependency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dépendance introuvable.",
        )

    # Vérifier que la dépendance appartient bien au projet
    dependencies = get_dependencies(
        db=db,
        project_id=project_id,
    )

    if dependency not in dependencies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dépendance introuvable dans ce projet.",
        )

    delete_dependency(
        db=db,
        dependency=dependency,
    )

    return None