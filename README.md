# Ticket Booking System

A FastAPI-based ticket booking system that allows users to book tickets for events.

## Features

- User management (create, view users)
- Event management (create, view events)
- Booking management (create, view bookings)
- Capacity checking for events
- Date validation for bookings
- Duplicate booking prevention
- Past event booking prevention

## Tech Stack

- Python 3.x
- FastAPI
- MySQL
- mysql-connector-python
- Pydantic

## Setup

1. Clone the repository:
```bash
git clone https://github.com/MohamdOmar/ticket_booking_system.git
cd ticket_booking_system
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
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

## API Endpoints and Examples

### Users

#### 1. Create a new user
- **Endpoint**: `POST /users/`
- **Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```
- **Example**:
```bash
curl -X 'POST' \
  'http://localhost:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "John Doe",
  "email": "john@example.com"
}'
```

#### 2. Get all users
- **Endpoint**: `GET /users/`
- **Example**:
```bash
curl -X 'GET' \
  'http://localhost:8000/users/' \
  -H 'accept: application/json'
```

#### 3. Get a specific user
- **Endpoint**: `GET /users/{user_id}`
- **Example**:
```bash
curl -X 'GET' \
  'http://localhost:8000/users/1' \
  -H 'accept: application/json'
```

### Events

#### 1. Create a new event
- **Endpoint**: `POST /events/`
- **Request Body**:
```json
{
  "name": "Summer Concert",
  "date": "2024-07-15",
  "capacity": 100
}
```
- **Example**:
```bash
curl -X 'POST' \
  'http://localhost:8000/events/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Summer Concert",
  "date": "2024-07-15",
  "capacity": 100
}'
```

#### 2. Get all events
- **Endpoint**: `GET /events/`
- **Example**:
```bash
curl -X 'GET' \
  'http://localhost:8000/events/' \
  -H 'accept: application/json'
```

#### 3. Get a specific event
- **Endpoint**: `GET /events/{event_id}`
- **Example**:
```bash
curl -X 'GET' \
  'http://localhost:8000/events/1' \
  -H 'accept: application/json'
```

### Bookings

#### 1. Create a new booking
- **Endpoint**: `POST /bookings/`
- **Request Body**:
```json
{
  "user_id": 1,
  "event_id": 1
}
```
- **Example**:
```bash
curl -X 'POST' \
  'http://localhost:8000/bookings/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 1,
  "event_id": 1
}'
```

#### 2. Get all bookings
- **Endpoint**: `GET /bookings/`
- **Example**:
```bash
curl -X 'GET' \
  'http://localhost:8000/bookings/' \
  -H 'accept: application/json'
```

#### 3. Get bookings for a specific event
- **Endpoint**: `GET /events/{event_id}/bookings`
- **Example**:
```bash
curl -X 'GET' \
  'http://localhost:8000/events/1/bookings' \
  -H 'accept: application/json'
```

#### 4. Get bookings for a specific user
- **Endpoint**: `GET /users/{user_id}/bookings`
- **Example**:
```bash
curl -X 'GET' \
  'http://localhost:8000/users/1/bookings' \
  -H 'accept: application/json'
```

## Error Handling

The API handles various error cases:
- Invalid user/event IDs (404 Not Found)
- Duplicate email addresses (400 Bad Request)
- Duplicate bookings (400 Bad Request)
- Past event bookings (400 Bad Request)
- Event capacity exceeded (400 Bad Request)
