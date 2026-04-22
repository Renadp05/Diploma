from fastapi import APIRouter
from pydantic import BaseModel

from app.services.tron_sender import send_trx
from app.services.token_service import transfer_trc20


router = APIRouter()


class SendTRXRequest(BaseModel):
    to_address: str
    amount_sun: int


class SendTokenRequest(BaseModel):
    to_address: str
    amount: int


@router.post("/send-trx")
def send_trx_route(data: SendTRXRequest):
    return send_trx(
        to_address=data.to_address,
        amount_sun=data.amount_sun,
    )


@router.post("/send-token")
def send_token_route(data: SendTokenRequest):
    return transfer_trc20(
        to_address=data.to_address,
        amount=data.amount,
    )