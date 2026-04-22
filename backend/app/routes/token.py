from fastapi import APIRouter
from pydantic import BaseModel

from app.services.token_service import transfer_trc20

router = APIRouter()


class TransferRequest(BaseModel):
    to_address: str
    amount: int


@router.post("/transfer")
def transfer_token(data: TransferRequest):
    return transfer_trc20(
        to_address=data.to_address,
        amount=data.amount,
    )