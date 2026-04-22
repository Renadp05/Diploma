from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import get_setting
from app.utils.database import Base, engine
from app.middleware.audit import AuditMiddleware
from app.routes import auth, dashboard, logs, nft, risk, simulation, transaction

app = FastAPI(title="TRC Backend - Secure Version")
app.add_middleware(AuditMiddleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])
app.include_router(nft.router, prefix="/nft", tags=["NFT"])
app.include_router(risk.router, prefix="/risk", tags=["Risk"])
app.include_router(simulation.router, prefix="/simulation", tags=["Simulation"])
app.include_router(transaction.router, prefix="/transaction", tags=["Transaction"])


@app.get("/")
def root():
    return {
        "status": "running",
        "project": "TRC Secure Backend",
        "network": get_setting("TRON_NETWORK", "shasta"),
    }