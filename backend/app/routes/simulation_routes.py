from fastapi import APIRouter, Query
from app.services.tron_sender import get_wallet_info, send_trx

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.get("/fake")
def fake_transaction_demo():
    return {
        "mode": "DEMO",
        "type": "FAKE_TRANSACTION",
        "tx_found": False,
        "address_valid": False,
        "risk_level": "HIGH",
        "message": "This is simulated data for academic demonstration only"
    }


@router.get("/real")
def real_transaction_demo():
    return {
        "mode": "DEMO",
        "type": "REALISTIC_TRANSACTION",
        "tx_found": True,
        "address_valid": True,
        "risk_level": "LOW",
        "message": "This is simulated data for academic demonstration only"
    }


@router.get("/compare")
def compare_demo():
    return {
        "real": real_transaction_demo(),
        "fake": fake_transaction_demo()
    }


@router.get("/wallet")
def demo_wallet():
    return get_wallet_info()


@router.post("/send-demo")
def send_demo(
    to_address: str = Query(...),
    amount_sun: int = Query(1000000)
):
    return send_trx(to_address=to_address, amount_sun=amount_sun)