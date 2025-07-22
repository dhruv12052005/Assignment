from sqlalchemy.orm import Session
from .models import Offer
from .schemas import OfferCreate
from typing import List, Optional
from sqlalchemy import and_

def get_offer_by_title_and_bank(db: Session, title: str, bank_name: str) -> Optional[Offer]:
    return db.query(Offer).filter(Offer.title == title, Offer.bank_name == bank_name).first()

def create_offers(db: Session, offers: List[OfferCreate]) -> int:
    new_count = 0
    for offer in offers:
        existing = get_offer_by_title_and_bank(db, offer.title, offer.bank_name)
        if not existing:
            db_offer = Offer(
                bank_name=offer.bank_name,
                title=offer.title,
                offer_type=offer.offer_type,
                discount_value=offer.discount_value,
                max_discount=offer.max_discount,
                payment_instruments=offer.payment_instruments,
            )
            db.add(db_offer)
            new_count += 1
    db.commit()
    return new_count

def get_offers_for_bank(db: Session, bank_name: str, payment_instrument: Optional[str] = None) -> List[Offer]:
    query = db.query(Offer).filter(Offer.bank_name == bank_name)
    if payment_instrument:
        query = query.filter(Offer.payment_instruments.like(f"%{payment_instrument}%"))
    return query.all()
