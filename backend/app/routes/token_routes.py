from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.services import token_service
from app.services.address_validator import validate_tron_address
from app.services.log_service import save_log
from app.utils.deps import get_current_user

router = APIRouter(prefix="/token", tags=["TRC-20 Token"])


class TransferRequest(BaseModel):
    to_address: str = Field(..., description="Recipient TRON address (Base58, starts with T...)")
    amount: float = Field(..., gt=0, description="Amount in USSDT (human-readable)")


class MintRequest(BaseModel):
    to_address: str = Field(..., description="TRON address to receive the freshly minted tokens")
    amount: float = Field(..., gt=0, description="Amount in USSDT (human-readable)")


@router.get("/info")
def token_info(current_user: dict = Depends(get_current_user)):
    info = token_service.get_token_info()
    if info.get("status") != "success":
        raise HTTPException(status_code=502, detail=info.get("message", "Token query failed"))

    save_log(
        user_id=current_user["user_id"],
        action="TOKEN_INFO",
        details=str({"contract": info["contract"], "network": info["network"]}),
    )
    return info


@router.get("/balance/{address}")
def token_balance(address: str, current_user: dict = Depends(get_current_user)):
    address_check = validate_tron_address(address)
    if not address_check.get("valid", False):
        raise HTTPException(status_code=400, detail=f"Invalid TRON address: {address}")

    result = token_service.get_balance(address)
    if result.get("status") != "success":
        raise HTTPException(status_code=502, detail=result.get("message", "Balance query failed"))

    save_log(
        user_id=current_user["user_id"],
        action="TOKEN_BALANCE",
        details=str({
            "address": address,
            "balance": result["balance"],
            "contract": result["contract"],
        }),
    )
    return result


@router.post("/transfer")
def token_transfer(payload: TransferRequest, current_user: dict = Depends(get_current_user)):
    address_check = validate_tron_address(payload.to_address)
    if not address_check.get("valid", False):
        raise HTTPException(status_code=400, detail=f"Invalid TRON address: {payload.to_address}")

    result = token_service.transfer(payload.to_address, payload.amount)

    save_log(
        user_id=current_user["user_id"],
        action="TOKEN_TRANSFER",
        details=str({
            "to": payload.to_address,
            "amount": payload.amount,
            "status": result.get("status"),
            "tx_id": result.get("tx_id"),
        }),
    )

    if result.get("status") != "success":
        raise HTTPException(status_code=502, detail=result.get("message", "Transfer failed"))

    return result


@router.post("/mint")
def token_mint(payload: MintRequest, current_user: dict = Depends(get_current_user)):
    address_check = validate_tron_address(payload.to_address)
    if not address_check.get("valid", False):
        raise HTTPException(status_code=400, detail=f"Invalid TRON address: {payload.to_address}")

    result = token_service.mint(payload.to_address, payload.amount)

    save_log(
        user_id=current_user["user_id"],
        action="TOKEN_MINT",
        details=str({
            "to": payload.to_address,
            "amount": payload.amount,
            "status": result.get("status"),
            "tx_id": result.get("tx_id"),
        }),
    )

    if result.get("status") != "success":
        raise HTTPException(status_code=502, detail=result.get("message", "Mint failed"))

    return result