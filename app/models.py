from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String, index=True)
    title = Column(String)
    offer_type = Column(String)  # e.g., FLAT, PERCENT
    discount_value = Column(Float)  # flat amount or % value
    max_discount = Column(Float, nullable=True)  # max cap in case of %
    payment_instruments = Column(String)  # comma-separated values
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("title", "bank_name", name="_bank_offer_uc"),)
