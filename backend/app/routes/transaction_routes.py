from fastapi import APIRouter, Query, Depends
from app.services.tron_rpc import (
    detect_network,
    calculate_confirmations,
    get_transaction,
    get_transaction_info,
)
from app.services.address_validator import validate_tron_address
from app.services.contract_checker import verify_contract
from app.services.risk_engine import compute_risk_score
from app.services.log_service import save_log
from app.services.transaction_service import save_transaction
from app.utils.deps import get_current_user

router = APIRouter(prefix="/tx", tags=["Transactions"])


@router.get("/{tx_id}/risk-analysis")
def risk_analysis(
    tx_id: str,
    wallet_address: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    tx = get_transaction(tx_id)
    tx_info = get_transaction_info(tx_id)
    tx_found = bool(tx_info or tx)

    network_status = detect_network()

    address_result = validate_tron_address(wallet_address)
    address_valid = address_result.get("valid", False)

    confirmations = calculate_confirmations(tx_id)

    contract_address = None
    if tx_info and isinstance(tx_info, dict):
        contract_address = tx_info.get("contract_address")

        if not contract_address:
            logs = tx_info.get("log", [])
            if logs and isinstance(logs, list):
                contract_address = logs[0].get("address")

    contract_result = verify_contract(contract_address)

    risk_result = compute_risk_score(
        tx_found=tx_found,
        address_valid=address_valid,
        confirmations=confirmations,
        contract_verified=contract_result["verified"],
        network_status=network_status
    )

    save_log(
    user_id=current_user["user_id"],
    action="RISK_ANALYSIS",
    details=str({
        "tx_id": tx_id,
        "wallet_address": wallet_address,
        "network_status": network_status,
        "confirmations": confirmations,
        "address_valid": address_valid,
        "contract_result": contract_result,
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"]
    })
)

    save_transaction({
        "tx_hash": tx_id,
        "wallet_address": wallet_address,
        "chain_type": network_status,
        "status": "FOUND" if tx_found else "NOT_FOUND",
        "confirmations": confirmations,
        "contract_address": contract_address,
        "risk_score": risk_result["risk_score"],
        "final_result": risk_result["risk_level"],
    })

    return {
        "tx_id": tx_id,
        "wallet_address": wallet_address,
        "tx_found": tx_found,
        "network_status": network_status,
        "confirmations": confirmations,
        "address_valid": address_valid,
        "address_validation": address_result,
        "contract_result": contract_result,
        "risk_result": risk_result,
        "checked_by": current_user["username"]
    }