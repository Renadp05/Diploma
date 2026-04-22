import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
TRON_RPC = os.getenv("TRON_RPC", "https://api.trongrid.io")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")