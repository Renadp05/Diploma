from app.models.user_model import users_db
from app.utils.security import verify_password, create_token


def authenticate_user(username: str, password: str):

    user = users_db.get(username)

    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    return user


def login_user(username: str, password: str):

    user = authenticate_user(username, password)

    if not user:
        return {"error": "Invalid credentials"}

    token = create_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "role": user["role"]
    }