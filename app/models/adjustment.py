from sqlalchemy import Column, Integer, Numeric, DateTime, func
from ..database import Base

class Adjustment(Base):
    __tablename__ = 'adjustments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    currency_id = Column(Integer, nullable=False)
    amount = Column(Numeric(16, 2), nullable=False)
    base_currency_closing_rate = Column(Numeric(32, 4), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, id=None, user_id=None, currency_id=None, amount=None, base_currency_closing_rate=None):
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id
        self.amount = amount
        self.base_currency_closing_rate = base_currency_closing_rate
