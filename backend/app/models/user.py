from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
 
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False, default="USER")

    isActive = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )