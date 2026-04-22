from datetime import datetime
from app.utils.database import SessionLocal
from app.models.log_model import Log


def save_log(user_id: int, action: str, details: str):
    db = SessionLocal()

    try:
        log = Log(
            user_id=user_id,
            action=action,
            timestamp=datetime.utcnow().isoformat(),
            details=details
        )

        db.add(log)
        db.commit()
        db.refresh(log)
    finally:
        db.close()


def get_logs():
    db = SessionLocal()

    try:
        logs = db.query(Log).order_by(Log.id.desc()).all()

        return [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "timestamp": log.timestamp,
                "details": log.details
            }
            for log in logs
        ]
    finally:
        db.close()