from sqlalchemy import Column, Integer, Numeric, DateTime, func
from ..database import Base

class InterbankDeal(Base):
    __tablename__ = 'interbank_deals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    currency_id = Column(Integer, nullable=False)
    interoffice_rate = Column(Numeric(32, 4), nullable=False)
    base_currency_closing_rate = Column(Numeric(32, 4), nullable=False)
    amount = Column(Numeric(32, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, id=None, user_id=None, currency_id=None, interoffice_rate=None, base_currency_closing_rate=None, amount=None):
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id
        self.interoffice_rate = interoffice_rate
        self.base_currency_closing_rate = base_currency_closing_rate
        self.amount = amount
