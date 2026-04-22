from datetime import datetime, timedelta
from typing import Any

from app.models.transaction_model import Transaction
from app.utils.database import SessionLocal


def save_transaction(data: dict[str, Any]) -> None:
    db = SessionLocal()

    try:
        created_at = datetime.utcnow()
        valid_until = created_at + timedelta(days=180)

        tx = Transaction(
            tx_hash=data.get("tx_hash"),
            wallet_address=data.get("wallet_address"),
            chain_type=data.get("chain_type"),
            status=data.get("status"),
            confirmations=int(data.get("confirmations", 0) or 0),
            contract_address=data.get("contract_address"),
            risk_score=data.get("risk_score"),
            final_result=data.get("final_result"),
            created_at=str(created_at),
            valid_until=str(valid_until),
        )

        db.add(tx)
        db.commit()
        db.refresh(tx)
    finally:
        db.close()