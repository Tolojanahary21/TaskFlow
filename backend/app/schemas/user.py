from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    role: str = "USER"
    isActive: bool = True


class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None
    isActive: bool | None = None


class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    role: str
    isActive: bool
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True