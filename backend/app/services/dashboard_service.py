import ast
from app.services.log_service import get_logs


def classify_risk(score: int) -> str:
    if score < 30:
        return "Verified"
    elif score < 70:
        return "Suspicious"
    return "High Risk"


def get_dashboard_data():
    logs = get_logs()

    total = len(logs)
    verified = 0
    suspicious = 0
    high_risk = 0

    enriched_logs = []

    for log in logs:
        score = 0

        try:
            details = ast.literal_eval(log.get("details", "{}"))
            if isinstance(details, dict):
                score = int(details.get("risk_score", 0))
        except Exception:
            score = 0

        category = classify_risk(score)

        if category == "Verified":
            verified += 1
        elif category == "Suspicious":
            suspicious += 1
        else:
            high_risk += 1

        enriched_log = log.copy()
        enriched_log["risk_score"] = score
        enriched_log["risk_category"] = category
        enriched_logs.append(enriched_log)

    latest = enriched_logs[:5]

    return {
        "total": total,
        "verified": verified,
        "suspicious": suspicious,
        "high_risk": high_risk,
        "latest_transactions": latest
    }