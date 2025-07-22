from .schemas import OfferCreate
from typing import List

def parse_flipkart_offers(api_response: dict) -> List[OfferCreate]:
    offers = []
    payment_offers = api_response.get('data', {}).get('paymentOffers', [])
    for offer in payment_offers:
        offers.append(
            OfferCreate(
                bank_name=offer.get('bankName', ''),
                title=offer.get('title', ''),
                offer_type=offer.get('offerType', ''),
                discount_value=offer.get('discountValue', 0),
                max_discount=offer.get('maxDiscount'),
                payment_instruments=','.join(offer.get('paymentInstruments', [])),
            )
        )
    return offers
