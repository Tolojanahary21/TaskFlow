from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User

from ..crud.project import (
    create_project,
    get_projects,
    get_project,
    update_project,
    delete_project,
)
from ..database import get_db
from ..schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/", response_model=ProjectResponse)
def create(project: ProjectCreate, db: Session = Depends(get_db)):

    new_project = create_project(db, project)

    if not new_project:
        owner = db.query(User).filter(User.id == project.owner_id).first()
        if not owner:
            raise HTTPException(
            status_code=404,
            detail="Owner not founddd"
            )
        raise HTTPException(
        status_code=400,
        detail="End date cannot be before start date"
    )
        

    return new_project


@router.get("/", response_model=list[ProjectResponse])
def get_all(db: Session = Depends(get_db)):
    return get_projects(db)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_one(project_id: int, db: Session = Depends(get_db)):
    project = get_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    try:
        project = update_project(db, project_id, project_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not Found"
        )

    return project


@router.delete("/{project_id}")
def delete(project_id: int, db: Session = Depends(get_db)):
    project = delete_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "message": "Project deleted successfully"
    }