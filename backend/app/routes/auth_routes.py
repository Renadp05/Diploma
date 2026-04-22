from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.database import SessionLocal
from app.models.user_model import User
from app.utils.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == data.username).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    finally:
        db.close()