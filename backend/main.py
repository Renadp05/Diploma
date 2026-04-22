from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import get_setting
from app.utils.database import Base, engine
from app.middleware.audit import AuditMiddleware
# Routers (shtoji sipas strukturës tënde nëse ndryshojnë)
from app.routes import auth, users, token, tron

app = FastAPI(title="TRC Backend - Secure Version")
app.add_middleware(AuditMiddleware)

# CORS
origins = ["*"]  # mund ta kufizosh më vonë

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB INIT
Base.metadata.create_all(bind=engine)

# ROUTES
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(token.router, prefix="/token", tags=["Token"])
app.include_router(tron.router, prefix="/tron", tags=["Tron"])


@app.get("/")
def root():
    return {
        "status": "running",
        "project": "TRC Secure Backend",
        "network": get_setting("TRON_NETWORK", "shasta"),
    }