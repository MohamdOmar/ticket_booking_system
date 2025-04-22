# Ticket Booking System

A FastAPI-based ticket booking system that allows users to book tickets for events.

## Features

- User management (create, view users)
- Event management (create, view events)
- Booking management (create, view bookings)
- Capacity checking for events
- Date validation for bookings

## Tech Stack

- Python 3.x
- FastAPI
- MySQL
- SQLAlchemy
- Pydantic

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ticket_booking_system.git
cd ticket_booking_system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python init_database.py
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Users
- POST /users/ - Create a new user
- GET /users/ - Get all users
- GET /users/{user_id} - Get a specific user

### Events
- POST /events/ - Create a new event
- GET /events/ - Get all events
- GET /events/{event_id} - Get a specific event

### Bookings
- POST /bookings/ - Create a new booking
- GET /bookings/ - Get all bookings
- GET /events/{event_id}/bookings - Get bookings for an event
- GET /users/{user_id}/bookings - Get bookings for a user

## License

MIT 