from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.sql import func

from ..database import Base


class Task(Base):
    __tablename__ = "tasks"

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

    status_id = Column(
        Integer,
        ForeignKey("task_statuses.id"),
        nullable=False,
        index=True
    )

    assignee_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    priority = Column(
        String(20),
        nullable=False,
        default="MEDIUM"
    )

    complexity = Column(
        String(20),
        nullable=False,
        default="MEDIUM"
    )

    task_type = Column(
        String(30),
        nullable=False,
        default="FEATURE"
    )

    estimated_duration = Column(
        Integer,
        nullable=True
    )

    predicted_duration = Column(
        Integer,
        nullable=True
    )

    actual_duration = Column(
        Integer,
        nullable=True
    )

    progress = Column(
        Integer,
        nullable=False,
        default=0
    )

    start_date = Column(
        DateTime(timezone=True),
        nullable=True
    )

    due_date = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "progress >= 0 AND progress <= 100",
            name="ck_task_progress"
        ),

        CheckConstraint(
            "estimated_duration IS NULL OR estimated_duration > 0",
            name="ck_task_estimated_duration"
        ),

        CheckConstraint(
            "predicted_duration IS NULL OR predicted_duration > 0",
            name="ck_task_predicted_duration"
        ),

        CheckConstraint(
            "actual_duration IS NULL OR actual_duration > 0",
            name="ck_task_actual_duration"
        ),

        CheckConstraint(
            "start_date IS NULL OR due_date IS NULL OR start_date <= due_date",
            name="ck_task_dates"
        ),

        CheckConstraint(
            "completed_at IS NULL OR start_date IS NULL OR completed_at >= start_date",
            name="ck_task_completed_date"
        ),
    )