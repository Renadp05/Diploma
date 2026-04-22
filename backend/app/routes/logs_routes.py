from fastapi import APIRouter, Depends
from app.services.log_service import get_logs
from app.utils.deps import get_current_user

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/")
def all_logs(current_user: dict = Depends(get_current_user)):
    return {
        "user": current_user,
        "logs": get_logs()
    }