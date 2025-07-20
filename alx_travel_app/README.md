## Milestone 5: ALX_TRAVEL_APP

### Django milestone application

**Background Task Management and Email Notification Implementation with Celery and RabbitMQ**

---

### Description

This milestone focuses on implementing background task management and email notification functionality into the ALX Travel App using Celery as the task queue and RabbitMQ as the message broker. The system handles asynchronous tasks such as email notifications for booking confirmations, payment receipts, and user communications without blocking the main application flow.

### Features

- **Background Task Processing**: Asynchronous task execution using Celery workers.
- **Email Notifications**: Automated email sending for booking confirmations and payment receipts.
- **Message Queue Integration**: RabbitMQ as the message broker for reliable task queuing.
- **Task Monitoring**: Built-in task status tracking and monitoring capabilities.
- **Scalable Architecture**: Distributed task processing for improved performance.
- **Booking & Payment Models**: Enhanced models with email notification triggers.
- **API Endpoints**: RESTful endpoints integrated with background task triggers.
- **Authentication**: Secured endpoints with session and basic authentication.
- **Email Templates**: HTML email templates for professional user communications.
- **Task Retry Logic**: Automatic retry mechanisms for failed email delivery.

### Technologies Used

- **Django**: High-level Python web framework.
- **Django REST Framework**: Toolkit for building Web APIs.
- **Celery**: Distributed task queue for background processing.
- **RabbitMQ**: Message broker for task queuing and distribution.
- **Redis**: Optional result backend for task result storage.
- **SMTP**: Email delivery service integration.
- **SQLite**: Default database for development.
- **Postman**: For API testing.
- **Flower**: Web-based tool for monitoring Celery tasks (optional).

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   ```
2. **Install Dependencies**:
   ```bash
   cd alx_travel_app_0x03
   pip install -r requirements.txt
   ```
3. **Install and Start RabbitMQ**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install rabbitmq-server
   sudo systemctl start rabbitmq-server
   
   # macOS
   brew install rabbitmq
   brew services start rabbitmq
   ```
4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start Celery Worker** (in a separate terminal):
   ```bash
   celery -A alx_travel_app worker --loglevel=info
   ```
6. **Start Celery Beat** (for periodic tasks, in another terminal):
   ```bash
   celery -A alx_travel_app beat --loglevel=info
   ```
7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

### Usage

- Access the app at `http://localhost:8000`.
- API documentation (if enabled) at `http://localhost:8000/swagger/`.
- Test email notification endpoints using Postman or similar tools.
- Monitor Celery tasks using Flower at `http://localhost:5555` (if installed).
- Background tasks are automatically triggered on booking creation and payment completion.
- Email notifications are sent asynchronously without blocking the API response.
- Check RabbitMQ management interface at `http://localhost:15672` (guest/guest) for queue monitoring.

---
