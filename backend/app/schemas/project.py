from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    start_date: date
    end_date: date | None = None
    status: str = "PLANNING"
    owner_id: int

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None
    owner_id: int | None = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    start_date: date
    end_date: date | None
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

model_config = ConfigDict(from_attributes=True)