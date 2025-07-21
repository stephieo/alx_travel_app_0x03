# TODO - ALX Travel App

## PythonAnywhere Deployment

### Database Issues

- [ ] Troubleshoot the database connection and table creation issues
  - [ ] Verify database migrations are properly applied
  - [ ] Check if `listings_user` table exists in the database
  - [ ] Ensure all model tables are created correctly
  - [ ] Verify database credentials and connection settings

### Celery Setup

- [ ] Set up Celery for asynchronous task processing
  - [ ] Configure Celery worker processes
  - [ ] Set up Celery beat for scheduled tasks
  - [ ] Test email sending functionality with Celery tasks
  - [ ] Configure Celery logging and monitoring

### RabbitMQ Setup

- [ ] Set up RabbitMQ as message broker for Celery
  - [ ] Install and configure RabbitMQ on PythonAnywhere
  - [ ] Configure Celery to use RabbitMQ as broker
  - [ ] Set up RabbitMQ user permissions and virtual hosts
  - [ ] Test message queue functionality

### Alternative Solution

- [ ] Check out using Railway if Celery + RabbitMQ doesn't work
  - [ ] Research Railway deployment options
  - [ ] Compare Railway vs PythonAnywhere for background tasks
  - [ ] Evaluate cost and performance differences
  - [ ] Plan migration strategy if needed

## Other Tasks

- [x] Fix the corrupted seed.py file
- [ ] Complete database seeding functionality
- [ ] Test all application features in production environment
