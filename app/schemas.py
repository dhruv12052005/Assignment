from pydantic import BaseModel, Field
from typing import Optional, List

class OfferBase(BaseModel):
    bank_name: str
    title: str
    offer_type: str  # FLAT or PERCENT
    discount_value: float
    max_discount: Optional[float] = None
    payment_instruments: str  # comma-separated values

class OfferCreate(OfferBase):
    pass

class OfferOut(OfferBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True

class OfferRequest(BaseModel):
    flipkartOfferApiResponse: dict

class OfferResponse(BaseModel):
    noOfOffersIdentified: int
    noOfNewOffersCreated: int

class HighestDiscountResponse(BaseModel):
    highestDiscountAmount: float
