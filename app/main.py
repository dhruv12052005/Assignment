from fastapi import FastAPI
from .routes import offers

app = FastAPI()

app.include_router(offers.router)

@app.get("/")
def root():
    return {"message": "Flipkart Offer API Backend is running."}
