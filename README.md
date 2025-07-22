# Flipkart Offer API Backend

**Note:** I have assumed the Flipkart offer API response body. There were some issues in finding the exact API response from the Flipkart network tab, like there were two apis when i refresh the payment page but none of them contains details about offers. So, a generic Flipkart offer API structure was used to mimic the real behavior. 

---

## 1. Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run database migrations**
   - No manual migration needed; tables are auto-created on app start.
4. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Run tests**
   ```bash
   PYTHONPATH=. pytest tests/
   ```

---

## 2. Assumptions
- The Flipkart offer API response was assumed based on typical e-commerce payment offer APIs, as the exact response was not easily accessible.
- Offers are uniquely identified by their `title` and `bankName`.
- Payment instruments are stored as a comma-separated string.
- Only the fields required for discount calculation and filtering are stored.

---

## 3. Design Choices
- **Framework:** FastAPI was chosen for its speed, simplicity, and async support.
- **ORM:** SQLAlchemy for easy database interaction and future scalability (can switch to PostgreSQL easily).
- **Database:** SQLite for local development and simplicity; can be swapped for PostgreSQL in production.
- **Modular Code:** Models, schemas, CRUD, utils, and routes are separated for clarity and maintainability.
- **Testing:** Pytest is used for simple, reliable tests.

---

## 4. Scaling the GET /highest-discount Endpoint
- For 1,000 requests per second:
  - Use a production-grade database (e.g., PostgreSQL) with proper indexing on `bankName` and `paymentInstruments`.
  - Deploy with a performant ASGI server (e.g., Uvicorn with Gunicorn workers).
  - Add caching (e.g., Redis) for frequently requested scenarios.
  - Use connection pooling and optimize queries.

---

## 5. Improvements with More Time
- Add authentication and rate limiting.
- Improve error handling and input validation.
- Add support for more complex offer rules and expiry dates.
- Use Alembic for migrations.
- Add OpenAPI docs and more comprehensive tests.
- Containerize with Docker for easier deployment. 