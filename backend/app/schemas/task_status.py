from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskStatusCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    position: int = Field(default=0, ge=0)
    color: str | None = Field(default=None, max_length=20)


class TaskStatusUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    position: int | None = Field(
        default=None,
        ge=0
    )

    color: str | None = Field(
        default=None,
        max_length=20
    )


class TaskStatusResponse(BaseModel):
    id: int
    project_id: int
    name: str
    position: int
    color: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskStatusReorder(BaseModel):
    position: int = Field(ge=0)