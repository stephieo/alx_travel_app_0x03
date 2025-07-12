## Milestone 4: ALX_TRAVEL_APP

### Django milestone application

**Payment integration with Chapa**

---

### Description

This milestone focuses on integrating payment functionality into the ALX Travel App using Chapa as the payment gateway. Users can make secure payments for bookings, and the system handles payment initiation, verification, and callback processing.

### Features

- **Payment Integration**: Initiate and verify payments using the Chapa API.
- **Atomic Transactions**: Payment initiation is atomic to ensure data consistency.
- **Dynamic Payment References**: Unique transaction references are generated for each payment.
- **Booking & Payment Models**: Models for users, listings, bookings, and payments with proper relationships.
- **API Endpoints**: RESTful endpoints for listings, bookings, and payment operations.
- **Authentication**: Endpoints secured with session and basic authentication.
- **Callback Handling**: Handles Chapa payment callbacks to update payment status.
- **Extensible for Email Notifications**: (Planned) Email confirmation to users after payment via Celery.

### Technologies Used

- **Django**: High-level Python web framework.
- **Django REST Framework**: Toolkit for building Web APIs.
- **Chapa API**: Payment gateway for processing transactions.
- **SQLite**: Default database for development.
- **Postman**: For API testing.
- **requests**: For making external HTTP requests to Chapa.

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   ```
2. **Install Dependencies**:
   ```bash
   cd alx_travel_app_0x02
   pip install -r requirements.txt
   ```
3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
4. **Seed the Database** (optional):
   ```bash
   python manage.py loaddata initial_data.json
   ```
5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

### Usage

- Access the app at `http://localhost:8000`.
- API documentation (if enabled) at `http://localhost:8000/swagger/`.
- Test payment endpoints using Postman or similar tools.
- To initiate a payment, make a POST request to `/api/payments/initiate/` with a valid booking ID.
- After payment, Chapa will call your callback endpoint to update payment status.

---
