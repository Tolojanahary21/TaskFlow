from sqlalchemy.orm import Session

from ..models.task import Task
from ..models.task_dependency import TaskDependency


ALLOWED_DEPENDENCY_TYPES = {
    "BLOCKS",
    "PRECEDES",
}


def get_dependency(
    db: Session,
    dependency_id: int
):
    return (
        db.query(TaskDependency)
        .filter(TaskDependency.id == dependency_id)
        .first()
    )


def get_dependencies(
    db: Session,
    project_id: int
):
    return (
        db.query(TaskDependency)
        .join(
            Task,
            Task.id == TaskDependency.task_id
        )
        .filter(
            Task.project_id == project_id
        )
        .order_by(
            TaskDependency.created_at.desc()
        )
        .all()
    )


def dependency_creates_cycle(
    db: Session,
    task_id: int,
    depends_on_task_id: int
) -> bool:

    visited = set()
    stack = [depends_on_task_id]

    while stack:

        current_task_id = stack.pop()

        if current_task_id == task_id:
            return True

        if current_task_id in visited:
            continue

        visited.add(current_task_id)

        dependencies = (
            db.query(TaskDependency.depends_on_task_id)
            .filter(
                TaskDependency.task_id == current_task_id
            )
            .all()
        )

        for dependency in dependencies:
            stack.append(dependency[0])

    return False


def create_dependency(
    db: Session,
    project_id: int,
    data
):
    # Vérifier que les deux tâches existent
    task = (
        db.query(Task)
        .filter(
            Task.id == data.task_id,
            Task.project_id == project_id
        )
        .first()
    )

    depends_on_task = (
        db.query(Task)
        .filter(
            Task.id == data.depends_on_task_id,
            Task.project_id == project_id
        )
        .first()
    )

    if not task:
        raise ValueError(
            "La tâche principale n'existe pas dans ce projet."
        )

    if not depends_on_task:
        raise ValueError(
            "La tâche dépendante n'existe pas dans ce projet."
        )

    # Auto-dépendance
    if data.task_id == data.depends_on_task_id:
        raise ValueError(
            "Une tâche ne peut pas dépendre d'elle-même."
        )

    # Type de dépendance
    dependency_type = data.dependency_type.upper()

    if dependency_type not in ALLOWED_DEPENDENCY_TYPES:
        raise ValueError(
            f"Type de dépendance invalide. "
            f"Valeurs autorisées : {', '.join(ALLOWED_DEPENDENCY_TYPES)}"
        )

    # Vérifier le doublon
    existing = (
        db.query(TaskDependency)
        .filter(
            TaskDependency.task_id == data.task_id,
            TaskDependency.depends_on_task_id == data.depends_on_task_id
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Cette dépendance existe déjà."
        )

    # Vérifier le cycle
    if dependency_creates_cycle(
        db,
        data.task_id,
        data.depends_on_task_id
    ):
        raise ValueError(
            "Cette dépendance créerait un cycle."
        )

    dependency = TaskDependency(
        task_id=data.task_id,
        depends_on_task_id=data.depends_on_task_id,
        dependency_type=dependency_type
    )

    db.add(dependency)
    db.commit()
    db.refresh(dependency)

    return dependency


def delete_dependency(
    db: Session,
    dependency: TaskDependency
):
    db.delete(dependency)
    db.commit()