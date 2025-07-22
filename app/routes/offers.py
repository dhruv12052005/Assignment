from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud, utils
from typing import Optional

router = APIRouter()

@router.post("/offer", response_model=schemas.OfferResponse)
def create_offer(
    offer_req: schemas.OfferRequest,
    db: Session = Depends(get_db)
):
    offers = utils.parse_flipkart_offers(offer_req.flipkartOfferApiResponse)
    no_of_offers_identified = len(offers)
    no_of_new_offers_created = crud.create_offers(db, offers)
    return schemas.OfferResponse(
        noOfOffersIdentified=no_of_offers_identified,
        noOfNewOffersCreated=no_of_new_offers_created
    )

@router.get("/highest-discount", response_model=schemas.HighestDiscountResponse)
def get_highest_discount(
    amountToPay: float = Query(...),
    bankName: str = Query(...),
    paymentInstrument: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    offers = crud.get_offers_for_bank(db, bankName, paymentInstrument)
    max_discount = 0.0
    for offer in offers:
        if offer.offer_type.upper() == "FLAT":
            discount = offer.discount_value
        elif offer.offer_type.upper() == "PERCENT":
            discount = (amountToPay * offer.discount_value / 100.0)
            if offer.max_discount is not None:
                discount = min(discount, offer.max_discount)
        else:
            discount = 0.0
        if discount > max_discount:
            max_discount = discount
    return schemas.HighestDiscountResponse(highestDiscountAmount=max_discount)
