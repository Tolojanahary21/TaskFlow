from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.sql import func

from ..database import Base


class TaskStatus(Base):
    __tablename__ = "task_statuses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    position = Column(
        Integer,
        nullable=False,
        default=0
    )

    color = Column(
        String(20),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "name",
            name="uq_task_status_project_name"
        ),
    )