from typing import Any, List, Dict


def generate_alerts(data: dict[str, Any]) -> List[Dict[str, str]]:
    alerts: List[Dict[str, str]] = []

    tx_exists = bool(data.get("tx_exists", True))
    address_valid = bool(data.get("address_valid", True))
    contract_status = data.get("contract_status", "Unknown Contract")
    network = data.get("network", "UNKNOWN")
    status = data.get("status")
    confirmations = int(data.get("confirmations", 0) or 0)

    # 1. Transaction existence
    if not tx_exists:
        alerts.append({
            "level": "High Risk",
            "message": "Transaction not found"
        })

    # 2. Transaction status
    if status and status != "SUCCESS":
        alerts.append({
            "level": "Warning",
            "message": "Transaction failed or pending"
        })

    # 3. Address validation
    if not address_valid:
        alerts.append({
            "level": "Warning",
            "message": "Invalid address"
        })

    # 4. Contract issues
    if contract_status == "Unknown Contract":
        alerts.append({
            "level": "Warning",
            "message": "Unknown contract"
        })
    elif contract_status == "Suspicious Contract":
        alerts.append({
            "level": "High Risk",
            "message": "Potential scam contract detected"
        })
    elif contract_status == "No Transaction Data":
        alerts.append({
            "level": "Warning",
            "message": "No contract data available"
        })

    # 5. Network mismatch
    if network != "MAINNET":
        alerts.append({
            "level": "Warning",
            "message": "Network mismatch"
        })

    # 6. Confirmations
    if confirmations == 0:
        alerts.append({
            "level": "Warning",
            "message": "No confirmations"
        })
    elif confirmations < 3:
        alerts.append({
            "level": "Info",
            "message": "Low confirmations"
        })

    return alerts