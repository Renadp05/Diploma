from app.services.risk_engine import calculate_risk


def simulate_fake_transaction():

    data = {
        "status": "FAILED",
        "address_valid": False,
        "contract_status": "Suspicious Contract",
        "network": "UNKNOWN"
    }

    result = calculate_risk(data)

    return {
        "type": "FAKE",
        "analysis": result
    }


def simulate_real_transaction():

    data = {
        "status": "SUCCESS",
        "address_valid": True,
        "contract_status": "Verified Token Contract",
        "network": "MAINNET"
    }

    result = calculate_risk(data)

    return {
        "type": "REAL",
        "analysis": result
    }