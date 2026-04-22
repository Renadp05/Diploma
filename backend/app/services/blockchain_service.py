import random
from app.services.address_validator import validate_tron_address
from app.services.risk_engine import calculate_risk
from app.services.log_service import save_log


def simulate_transaction(tx: dict):
    sender_check = validate_tron_address(tx["sender"])
    receiver_check = validate_tron_address(tx["receiver"])

    if not sender_check["valid"] or not receiver_check["valid"]:
        return {"error": "Invalid sender or receiver address"}

    success = random.choice([True, True, False])

    risk_data = {
        "status": "SUCCESS" if success else "FAILED",
        "address_valid": True,
        "contract_status": "Verified Token Contract",
        "network": "MAINNET"
    }

    risk = calculate_risk(risk_data)

    save_log(
        user_id=1,
        action="simulate_transaction",
        details=str({
            "sender": tx["sender"],
            "receiver": tx["receiver"],
            "amount": tx["amount"],
            "success": success,
            "risk": risk
        })
    )

    return {
        "sender": tx["sender"],
        "receiver": tx["receiver"],
        "amount": tx["amount"],
        "success": success,
        "risk": risk
    }