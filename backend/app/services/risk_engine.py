def compute_risk_score(
    tx_found: bool,
    address_valid: bool,
    confirmations: int,
    contract_verified: bool,
    network_status: str
) -> dict:
    score = 0
    reasons = []

    if not tx_found:
        score += 40
        reasons.append("Transaction not found on blockchain")

    if not address_valid:
        score += 20
        reasons.append("Invalid wallet address")

    if confirmations == 0:
        score += 15
        reasons.append("No confirmations")

    if not contract_verified:
        score += 15
        reasons.append("Unverified or unknown contract")

    if network_status in ["UNKNOWN", "UNREACHABLE"]:
        score += 10
        reasons.append("Network could not be verified")

    if score <= 30:
        level = "LOW"
    elif score <= 70:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons
    }