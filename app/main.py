from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr, field_validator
from datetime import datetime, date
from . import db_utils
from .database import DatabaseError, NotFoundError, DuplicateBookingError, DuplicateUserError

app = FastAPI(
    title="Event Ticket Booking System",
    description="A simple API for booking event tickets",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
async def root():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs")

# Models that match MySQL data types
class User(BaseModel):
    name: constr(max_length=100)  # VARCHAR(100)
    email: EmailStr  # VARCHAR(100) with email validation

class Event(BaseModel):
    name: constr(max_length=200)  # VARCHAR(200)
    date: date  # DATE
    capacity: int  # INT

class Booking(BaseModel):
    user_id: int  # INT
    event_id: int  # INT

# User endpoints
@app.post("/users/", response_model=dict)
async def create_user_endpoint(user: User):
    try:
        return db_utils.create_user(user.name, user.email)
    except DuplicateUserError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/", response_model=List[dict])
async def get_users():
    try:
        return db_utils.get_all_users()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=dict)
async def get_user_endpoint(user_id: int):
    try:
        return db_utils.get_user_by_id(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Event endpoints
@app.post("/events/", response_model=dict)
async def create_event_endpoint(event: Event):
    try:
        return db_utils.create_event(event.name, event.date, event.capacity)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events/", response_model=List[dict])
async def get_events():
    try:
        return db_utils.get_all_events()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events/{event_id}", response_model=dict)
async def get_event_endpoint(event_id: int):
    try:
        return db_utils.get_event_by_id(event_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Booking endpoints
@app.post("/bookings/", response_model=dict)
async def create_booking_endpoint(booking: Booking):
    try:
        return db_utils.create_booking(booking.user_id, booking.event_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bookings/", response_model=List[dict])
async def get_bookings():
    try:
        return db_utils.get_all_bookings()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}/bookings", response_model=List[dict])
async def get_user_bookings_endpoint(user_id: int):
    try:
        return db_utils.get_user_bookings(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events/{event_id}/bookings", response_model=List[dict])
async def get_event_bookings_endpoint(event_id: int):
    try:
        return db_utils.get_event_bookings(event_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e)) 