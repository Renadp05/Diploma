from fastapi import APIRouter, Query
from typing import Dict

router = APIRouter(prefix="/risk", tags=["Risk Analysis"])


@router.get("/")
def risk_health() -> Dict[str, str]:
    """
    Health check endpoint for the risk analysis module.
    Confirms that the risk engine is operational.
    """
    return {"message": "Risk module operational"}


@router.get("/score")
def get_risk_score(score: int = Query(..., ge=0, le=100)) -> Dict[str, str | int]:
    """
    Classifies a given risk score into a risk level.

    Parameters:
    - score (int): Risk score between 0 and 100

    Returns:
    - score: numeric risk score
    - level: classified risk level
    """

    if score < 30:
        level = "Low Risk"
        description = "Transaction appears safe"
    elif score < 70:
        level = "Medium Risk"
        description = "Transaction requires further review"
    else:
        level = "High Risk"
        description = "Transaction is potentially dangerous"

    return {
        "score": score,
        "level": level,
        "description": description
    }