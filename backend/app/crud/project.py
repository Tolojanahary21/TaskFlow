from sqlalchemy.orm import Session

from ..models.user import User
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate

VALID_STATUSES = {
    "PLANNING",
    "IN_PROGRESS",
    "COMPLETED",
    "CANCELLED",
}
# Ajout 
def create_project(db: Session, project: ProjectCreate):
    # if dans les utilisateurs
    owner = db.query(User).filter(User.id == project.owner_id).first()
    if not owner:
        return None
    # verification des dates
    if project.end_date and project.end_date < project.start_date:
        return None
    # verification status 
    if project.status not in VALID_STATUSES:
        raise ValueError("Invalid project status")
    db_project = Project(
        name=project.name,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
        status=project.status,
        owner_id=project.owner_id,
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

# get all
def get_projects(db: Session):
    return db.query(Project).all()

# get by ID
def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

# UPDATE PROJECT
def update_project(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate
):
    db_project = get_project(db, project_id)

    if not db_project:
        return None

    update_data = project_data.model_dump(exclude_unset=True)
    # empecher associer a un user non existant 
    if "owner_id" in update_data:
        owner = db.query(User).filter(
        User.id == update_data["owner_id"]
    ).first()

    # verifier status
    if "status" in update_data:
        if update_data["status"] not in VALID_STATUSES:
            raise ValueError("Invalid project status")
        
    new_start_date = update_data.get("start_date", db_project.start_date)
    new_end_date = update_data.get("end_date", db_project.end_date)
    
    if new_end_date and new_end_date < new_start_date:
         raise ValueError("End date cannot be before start date")

    for field, value in update_data.items():
        setattr(db_project, field, value)

    db.commit()
    db.refresh(db_project)

    return db_project

# dELETE PROJECT
def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)

    if not db_project:
        return None

    db.delete(db_project)
    db.commit()

    return db_project