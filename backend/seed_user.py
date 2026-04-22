from datetime import datetime
from app.utils.database import SessionLocal
from app.models.user_model import User
from app.utils.security import hash_password

db = SessionLocal()

existing = db.query(User).filter(User.username == "admin").first()

if not existing:
    user = User(
        username="admin",
        password_hash=hash_password("admin123"),
        role="admin",
        created_at=str(datetime.utcnow())
    )
    db.add(user)
    db.commit()

db.close()
print("User created.")