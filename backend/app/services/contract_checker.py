from app.services.tron_rpc import get_transaction_info

TRUSTED_TRC20_CONTRACTS = {
    "USDT": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
}


def verify_contract(contract_address: str) -> dict:
    if not contract_address:
        return {
            "verified": False,
            "label": "Missing Contract",
            "message": "No contract address found",
            "token": None,
            "contract": None,
        }

    for token_name, trusted_address in TRUSTED_TRC20_CONTRACTS.items():
        if contract_address == trusted_address:
            return {
                "verified": True,
                "label": "Trusted Contract",
                "message": f"Contract matches trusted token: {token_name}",
                "token": token_name,
                "contract": contract_address,
            }

    return {
        "verified": False,
        "label": "Unknown Contract",
        "message": "Contract is not in the trusted contract list",
        "token": None,
        "contract": contract_address,
    }


def extract_contract_from_tx(tx_id: str) -> str | None:
    tx_info = get_transaction_info(tx_id)

    if not tx_info or not isinstance(tx_info, dict):
        return None

    logs = tx_info.get("log", [])
    if not logs:
        return None

    first_log = logs[0]
    return first_log.get("address")


def check_trc20_contract(tx_id: str) -> dict:
    contract_address = extract_contract_from_tx(tx_id)
    result = verify_contract(contract_address)

    return {
        "status": "Verified Token Contract" if result["verified"] else result["label"],
        "verified": result["verified"],
        "token": result["token"],
        "contract": result["contract"],
        "message": result["message"],
    }