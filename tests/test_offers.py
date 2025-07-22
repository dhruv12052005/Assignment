from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Offer
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_offers_table():
    db = SessionLocal()
    db.query(Offer).delete()
    db.commit()
    db.close()

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Flipkart Offer API Backend is running."

def test_post_offer_and_highest_discount():
    # Provided Flipkart offer API response
    payload = {
        "flipkartOfferApiResponse": {
            "data": {
                "paymentOffers": [
                    {
                        "bankName": "AXIS",
                        "title": "10% off on Axis Bank Credit Cards",
                        "offerType": "PERCENT",
                        "discountValue": 10,
                        "maxDiscount": 500,
                        "paymentInstruments": ["CREDIT", "EMI_OPTIONS"]
                    },
                    {
                        "bankName": "HDFC",
                        "title": "Flat ₹300 off on HDFC Debit Cards",
                        "offerType": "FLAT",
                        "discountValue": 300,
                        "maxDiscount": None,
                        "paymentInstruments": ["DEBIT"]
                    },
                    {
                        "bankName": "ICICI",
                        "title": "5% Cashback on ICICI Credit Cards EMI",
                        "offerType": "PERCENT",
                        "discountValue": 5,
                        "maxDiscount": 200,
                        "paymentInstruments": ["EMI_OPTIONS"]
                    }
                ]
            }
        }
    }
    # POST /offer
    response = client.post("/offer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["noOfOffersIdentified"] == 3
    assert data["noOfNewOffersCreated"] >= 1  # Could be 3 if DB is empty

    # GET /highest-discount for AXIS, amount 10000, CREDIT
    response = client.get("/highest-discount", params={"amountToPay": 10000, "bankName": "AXIS", "paymentInstrument": "CREDIT"})
    assert response.status_code == 200
    data = response.json()
    # 10% of 10000 = 1000, but maxDiscount is 500
    assert data["highestDiscountAmount"] == 500

    # GET /highest-discount for HDFC, amount 10000, DEBIT
    response = client.get("/highest-discount", params={"amountToPay": 10000, "bankName": "HDFC", "paymentInstrument": "DEBIT"})
    assert response.status_code == 200
    data = response.json()
    assert data["highestDiscountAmount"] == 300

    # GET /highest-discount for ICICI, amount 10000, EMI_OPTIONS
    response = client.get("/highest-discount", params={"amountToPay": 10000, "bankName": "ICICI", "paymentInstrument": "EMI_OPTIONS"})
    assert response.status_code == 200
    data = response.json()
    # 5% of 10000 = 500, but maxDiscount is 200
    assert data["highestDiscountAmount"] == 200
