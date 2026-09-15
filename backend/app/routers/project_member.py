from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.project import Project
from ..models.user import User
from ..models.project_member import ProjectMember
from ..schemas.project_member import (
    ProjectMemberCreate,
    ProjectMemberUpdate,
    ProjectMemberResponse,
    ProjectMemberRole
)
from ..crud.project_member import (
    get_project_member,
    get_project_members,
    create_project_member,
    update_project_member_role,
    delete_project_member
)


router = APIRouter(
    prefix="/projects/{project_id}/members",
    tags=["Project Members"]
)

@router.post(
    "",
    response_model=ProjectMemberResponse,
    status_code=status.HTTP_201_CREATED
)
def add_project_member(
    project_id: int,
    data: ProjectMemberCreate,
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

    # Vérifier l'utilisateur
    user = (
        db.query(User)
        .filter(User.id == data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Vérifier si le membre existe déjà
    existing_member = get_project_member(
        db,
        project_id,
        data.user_id
    )

    if existing_member:
        raise HTTPException(
            status_code=409,
            detail="User is already a member of this project"
        )

    # OWNER doit correspondre au owner du projet
    if data.role == ProjectMemberRole.OWNER:
        if project.owner_id != data.user_id:
            raise HTTPException(
                status_code=400,
                detail="Only the project owner can have the OWNER role"
            )

    return create_project_member(
        db,
        project_id,
        data.user_id,
        data.role
    )
# consulter les membres 
@router.get(
    "",
    response_model=list[ProjectMemberResponse]
)
def list_project_members(
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

    return get_project_members(
        db,
        project_id
    )
# update roles
@router.patch(
    "/{user_id}",
    response_model=ProjectMemberResponse
)
def update_member_role(
    project_id: int,
    user_id: int,
    data: ProjectMemberUpdate,
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

    member = get_project_member(
        db,
        project_id,
        user_id
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Project member not found"
        )

    # Ne pas modifier le rôle du propriétaire du projet
    if user_id == project.owner_id:
        raise HTTPException(
            status_code=403,
            detail="The project owner role cannot be changed"
        )

    # Impossible de donner OWNER à quelqu'un d'autre
    if data.role == ProjectMemberRole.OWNER:
        raise HTTPException(
            status_code=400,
            detail="The OWNER role belongs to the project owner"
        )

    return update_project_member_role(
        db,
        member,
        data.role
    )
# Delete members
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_project_member(
    project_id: int,
    user_id: int,
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

    member = get_project_member(
        db,
        project_id,
        user_id
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Project member not found"
        )

    # Protection du propriétaire
    if user_id == project.owner_id:
        raise HTTPException(
            status_code=403,
            detail="The project owner cannot be removed"
        )

    # Protection supplémentaire si le rôle est OWNER
    if member.role == ProjectMemberRole.OWNER.value:
        raise HTTPException(
            status_code=403,
            detail="An OWNER cannot be removed"
        )

    delete_project_member(
        db,
        member
    )

    return None