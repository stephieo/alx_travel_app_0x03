## Milestone 3: ALX_TRAVEL_APP

### Django milestone application

Model and Serializer Creation, Data Seeding, and API Endpoints

### Description

This milestone focuses on creating API endpoints for the ALX Travel App. The goal is to set up the foundational structure of the application and expose RESTful API endpoints for listings and bookings.

### Features

- **Model Creation**: Define models for the application, including fields and relationships.
- **Serializer Creation**: Create serializers to convert model instances to JSON and vice versa.
- **Data Seeding**: Populate the database with initial data for testing and development purposes.
- **ViewSet Configuration**: Implement ViewSets for Listing and Booking models to provide CRUD operations.
- **URL Routing**: Set up RESTful API endpoints using Django REST Framework's router.

### Technologies Used

- **Django**: A high-level Python web framework for building web applications.
- **Django REST Framework**: A powerful toolkit for building Web APIs in Django.
- **SQLite**: A lightweight database for development and testing.
- **Postman**: A collaboration platform for API development and testing.

### Setup Instructions

1. **Clone the Repository**: Clone the repository to your local machine.
   ```bash
   git clone <repository-url>
   ```
2. **Install Dependencies**: Navigate to the project directory and install the required dependencies.
   ```bash
   cd alx_travel_app_0x00
   pip install -r requirements.txt
   ```
3. **Run Migrations**: Apply the migrations to create the database schema.
   ```bash
   python manage.py migrate
   ```
4. **Seed the Database**: Run the data seeding script to populate the database with initial data.
   ```bash
   python manage.py loaddata initial_data.json
   ```
5. **Run the Development Server**: Start the Django development server to test the application.
   ```bash
   python manage.py runserver
   ```

### Usage

- Access the application in your web browser at `http://localhost:8000`.
- Use the Django admin interface to manage models and data at `http://localhost:8000/admin`.
- Test the API endpoints using Postman or any other API testing tool.
