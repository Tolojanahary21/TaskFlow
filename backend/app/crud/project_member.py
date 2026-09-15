from sqlalchemy.orm import Session

from ..models.project_member import ProjectMember
from ..models.project import Project
from ..models.user import User
from ..schemas.project_member import ProjectMemberRole


def get_project_member(
    db: Session,
    project_id: int,
    user_id: int
):
    return (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        )
        .first()
    )


def get_project_members(
    db: Session,
    project_id: int
):
    return (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )


def create_project_member(
    db: Session,
    project_id: int,
    user_id: int,
    role: ProjectMemberRole
):
    member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role=role.value
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


def update_project_member_role(
    db: Session,
    member: ProjectMember,
    role: ProjectMemberRole
):
    member.role = role.value

    db.commit()
    db.refresh(member)

    return member


def delete_project_member(
    db: Session,
    member: ProjectMember
):
    db.delete(member)
    db.commit()