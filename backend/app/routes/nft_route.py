from fastapi import APIRouter
from app.services.nft_service import mint_nft

router = APIRouter(prefix="/nft", tags=["NFT"])


@router.post("/mint")
def mint():
    return mint_nft()