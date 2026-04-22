from sqlalchemy import Column, Integer, String
from app.utils.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    tx_hash = Column(String, nullable=False, index=True)
    wallet_address = Column(String, nullable=False)

    chain_type = Column(String, nullable=False)  # TRON / ETH / BSC

    status = Column(String)  # SUCCESS / FAILED / PENDING
    confirmations = Column(Integer, default=0)

    contract_address = Column(String)

    risk_score = Column(Integer)
    final_result = Column(String)  # Low / Medium / High Risk

    created_at = Column(String, nullable=False)
    valid_until = Column(String)  # 🔥 për kërkesën 6 muaj