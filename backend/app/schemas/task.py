from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class TaskComplexity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class TaskType(str, Enum):
    FEATURE = "FEATURE"
    BUG = "BUG"
    IMPROVEMENT = "IMPROVEMENT"
    REFACTORING = "REFACTORING"
    DOCUMENTATION = "DOCUMENTATION"
    TEST = "TEST"


class TaskCreate(BaseModel):
    status_id: int
    assignee_id: int | None = None

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = None

    priority: TaskPriority = TaskPriority.MEDIUM

    complexity: TaskComplexity = TaskComplexity.MEDIUM

    task_type: TaskType = TaskType.FEATURE

    estimated_duration: int | None = Field(
        default=None,
        gt=0
    )

    predicted_duration: int | None = Field(
        default=None,
        gt=0
    )

    actual_duration: int | None = Field(
        default=None,
        gt=0
    )

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    start_date: datetime | None = None

    due_date: datetime | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_date is not None
            and self.due_date is not None
            and self.start_date > self.due_date
        ):
            raise ValueError(
                "start_date must be before or equal to due_date"
            )

        return self


class TaskUpdate(BaseModel):
    status_id: int | None = None
    assignee_id: int | None = None

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = None

    priority: TaskPriority | None = None
    complexity: TaskComplexity | None = None
    task_type: TaskType | None = None

    estimated_duration: int | None = Field(
        default=None,
        gt=0
    )

    predicted_duration: int | None = Field(
        default=None,
        gt=0
    )

    actual_duration: int | None = Field(
        default=None,
        gt=0
    )

    progress: int | None = Field(
        default=None,
        ge=0,
        le=100
    )

    start_date: datetime | None = None
    due_date: datetime | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_date is not None
            and self.due_date is not None
            and self.start_date > self.due_date
        ):
            raise ValueError(
                "start_date must be before or equal to due_date"
            )

        return self


class TaskStatusChange(BaseModel):
    status_id: int


class TaskAssign(BaseModel):
    assignee_id: int


class TaskProgressUpdate(BaseModel):
    progress: int = Field(
        ge=0,
        le=100
    )


class TaskResponse(BaseModel):
    id: int
    project_id: int
    status_id: int
    assignee_id: int | None

    title: str
    description: str | None

    priority: TaskPriority
    complexity: TaskComplexity
    task_type: TaskType

    estimated_duration: int | None
    predicted_duration: int | None
    actual_duration: int | None

    progress: int

    start_date: datetime | None
    due_date: datetime | None
    completed_at: datetime | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )