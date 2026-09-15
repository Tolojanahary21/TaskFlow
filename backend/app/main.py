from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models.user import User
from .models.project import Project

# Routersss 
from .routers.project import router as project_router
from .routers.user import router as user_router
from .services.refresh_token import (save_refresh_token,verify_refresh_token,refresh_access_token)
from .routers.project_member import router as project_member_router
from .routers.task_status import router as task_status_router
from .routers.task import router as task_router
from .routers.task_history import router as task_history_router


app = FastAPI(title="TaskFlow AI")


Base.metadata.create_all(bind=engine)

# fuction Routes
app.include_router(user_router)
app.include_router(project_router)
app.include_router(project_member_router)
app.include_router(task_status_router)
app.include_router(task_router)
app.include_router(task_history_router)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "TaskFlow AI fonctionne"}


# Refresh Token

@app.post("/test/refresh-token/{user_id}")
def test_refresh_token(
    user_id: int,
    db: Session = Depends(get_db)
):
    token = save_refresh_token(db, user_id)

    return {
        "message": "Refresh token créé",
        "refresh_token": token
    }
@app.post("/test/verify-refresh-token")
def test_verify_refresh_token(
    token: str,
    db: Session = Depends(get_db)
):
    refresh_token = verify_refresh_token(db, token)

    if not refresh_token:
        return {
            "valid": False,
            "message": "Refresh token invalide"
        }

    return {
        "valid": True,
        "message": "Refresh token valide",
        "user_id": refresh_token.user_id
    }
@app.post("/auth/refresh")
def refresh(
    token: str,
    db: Session = Depends(get_db)
):
    access_token = refresh_access_token(db, token)

    if not access_token:
        return {
            "success": False,
            "message": "Refresh token invalide ou expiré"
        }

    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer"
    }