from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List, Optional

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
    date: datetime
    capacity: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

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

class BookingResponse(BaseModel):
    id: int
    user: User
    event: Event
    created_at: datetime

    class Config:
        from_attributes = True 