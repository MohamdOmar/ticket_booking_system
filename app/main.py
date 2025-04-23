from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr, field_validator
from datetime import datetime, date
from . import db_utils
from .database import DatabaseError, NotFoundError, DuplicateBookingError, DuplicateUserError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Event Ticket Booking System",
    description="A simple API for booking event tickets",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
async def root():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs")

# Pydantic models for request/response validation
class UserBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    name: constr(min_length=1, max_length=200)
    date: date
    capacity: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    date: str  # Will be in YYYY-MM-DD format

    @field_validator('date', mode='before')
    def parse_date(cls, v):
        if isinstance(v, str):
            return v
        elif isinstance(v, (datetime, date)):
            return v.strftime('%Y-%m-%d')
        return str(v)

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    user_id: int
    event_id: int

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User endpoints
@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    try:
        return db_utils.create_user(user.name, user.email)
    except DuplicateUserError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    try:
        return db_utils.get_user_by_id(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/", response_model=List[User])
def get_users():
    try:
        return db_utils.get_all_users()
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Event endpoints
@app.post("/events/", response_model=Event)
def create_event(event: EventCreate):
    try:
        return db_utils.create_event(event.name, event.date, event.capacity)
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int):
    try:
        return db_utils.get_event_by_id(event_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/events/", response_model=List[Event])
def get_events():
    try:
        return db_utils.get_all_events()
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Booking endpoints
@app.post("/bookings/", response_model=Booking)
def create_booking(booking: BookingCreate):
    try:
        return db_utils.create_booking(booking.user_id, booking.event_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DuplicateBookingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/bookings/", response_model=List[Booking])
def get_bookings():
    try:
        return db_utils.get_all_bookings()
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/events/{event_id}/bookings", response_model=List[Booking])
def get_event_bookings(event_id: int):
    try:
        return db_utils.get_event_bookings(event_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}/bookings", response_model=List[Booking])
def get_user_bookings(user_id: int):
    try:
        return db_utils.get_user_bookings(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=str(e)) 