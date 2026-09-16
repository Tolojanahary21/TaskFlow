from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SubtaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255
    )
    description: str | None = None
    position: int = Field(
        default=0,
        ge=0
    )


class SubtaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )
    description: str | None = None
    position: int | None = Field(
        default=None,
        ge=0
    )
    is_completed: bool | None = None


class SubtaskResponse(BaseModel):
    id: int
    task_id: int
    title: str
    description: str | None
    is_completed: bool
    position: int
    created_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )