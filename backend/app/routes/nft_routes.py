# app/routes/nft_routes.py
from fastapi import APIRouter
import uuid

router = APIRouter(prefix="/nft", tags=["NFT"])

@router.post("/mint-demo")
def mint_nft_demo(owner: str):
    return {
        "nft_id": str(uuid.uuid4()),
        "standard": "TRC-721 (SIMULATED)",
        "owner": owner,
        "metadata": {
            "name": "SecureChain Certificate",
            "description": "Transaction verified and minted as NFT proof",
        },
        "status": "MINTED (DEMO)"
    }