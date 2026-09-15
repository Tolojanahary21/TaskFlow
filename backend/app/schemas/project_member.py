from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ProjectMemberRole(str, Enum):
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    MEMBER = "MEMBER"


class ProjectMemberCreate(BaseModel):
    user_id: int
    role: ProjectMemberRole = ProjectMemberRole.MEMBER


class ProjectMemberUpdate(BaseModel):
    role: ProjectMemberRole


class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: ProjectMemberRole
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)