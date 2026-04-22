from sqlalchemy import Column, Integer, String
from app.utils.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)

    timestamp = Column(String, nullable=False)

    details = Column(String)  # JSON string me info (risk_score, tx_id, etj.)