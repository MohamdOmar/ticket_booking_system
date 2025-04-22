from typing import List, Dict, Any, Optional
from datetime import datetime, date
import logging
from .database import execute_query, DatabaseError, NotFoundError, DuplicateBookingError

logger = logging.getLogger(__name__)

def create_user(name: str, email: str) -> int:
    """Create a new user and return their ID"""
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    try:
        return execute_query(query, (name, email), fetch=False)
    except DatabaseError as e:
        raise DatabaseError(f"Failed to create user: {str(e)}")

def get_user_by_id(user_id: int) -> Dict[str, Any]:
    """Get a user by their ID"""
    query = "SELECT * FROM users WHERE id = %s"
    result = execute_query(query, (user_id,))
    if not result:
        raise NotFoundError(f"User with ID {user_id} not found")
    return result[0]

def get_user_by_email(email: str) -> Dict[str, Any]:
    """Get a user by their email"""
    query = "SELECT * FROM users WHERE email = %s"
    result = execute_query(query, (email,))
    if not result:
        raise NotFoundError(f"User with email {email} not found")
    return result[0]

def get_all_users() -> List[Dict[str, Any]]:
    """Get all users"""
    query = "SELECT * FROM users"
    return execute_query(query)

def create_event(name: str, date: datetime, capacity: int) -> int:
    """Create a new event and return its ID."""
    try:
        # Format the date for MySQL
        mysql_date = date.strftime('%Y-%m-%d')
        
        query = "INSERT INTO events (name, date, capacity) VALUES (%s, %s, %s)"
        params = (name, mysql_date, capacity)
        
        return execute_query(query, params, fetch=False)
    except Exception as e:
        raise DatabaseError(f"Failed to create event: {str(e)}")

def get_event_by_id(event_id: int) -> dict:
    """Get an event by its ID."""
    try:
        query = "SELECT id, name, DATE(date) as date, capacity FROM events WHERE id = %s"
        result = execute_query(query, (event_id,))
        if not result:
            raise NotFoundError(f"Event with ID {event_id} not found")
        return result[0]
    except Exception as e:
        raise DatabaseError(f"Failed to get event: {str(e)}")

def get_all_events() -> List[dict]:
    """Get all events."""
    try:
        query = "SELECT id, name, DATE(date) as date, capacity FROM events"
        return execute_query(query)
    except Exception as e:
        raise DatabaseError(f"Failed to get events: {str(e)}")

def create_booking(user_id: int, event_id: int) -> dict:
    """Create a new booking with validation checks"""
    try:
        # Check if user exists
        user = get_user_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
            
        # Check if event exists
        event = get_event_by_id(event_id)
        if not event:
            raise NotFoundError(f"Event with ID {event_id} not found")
            
        # Check if event is in the past
        event_date = event['date']
        if isinstance(event_date, str):
            event_date = datetime.strptime(event_date, '%Y-%m-%d')
        elif isinstance(event_date, date):
            event_date = datetime.combine(event_date, datetime.min.time())
            
        if event_date < datetime.now():
            raise DatabaseError("Cannot book past events")
            
        # Check if event is at capacity
        current_bookings = get_booking_count(event_id)
        if current_bookings >= event['capacity']:
            raise DatabaseError("Event is at full capacity")
            
        # Create the booking
        query = "INSERT INTO bookings (user_id, event_id) VALUES (%s, %s)"
        booking_id = execute_query(query, (user_id, event_id), fetch=False)
        
        # Return the newly created booking
        return get_booking_by_id(booking_id)
        
    except Exception as e:
        raise DatabaseError(f"Failed to create booking: {str(e)}")

def get_booking_count(event_id: int) -> int:
    """Get the number of bookings for an event"""
    query = "SELECT COUNT(*) as count FROM bookings WHERE event_id = %s"
    result = execute_query(query, (event_id,))
    return result[0]['count']

def get_all_bookings() -> List[dict]:
    """Get all bookings with user and event details"""
    query = """
        SELECT b.*, u.name as user_name, e.name as event_name, e.date as event_date
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN events e ON b.event_id = e.id
    """
    return execute_query(query)

def get_event_bookings(event_id: int) -> List[dict]:
    """Get all bookings for a specific event"""
    query = """
        SELECT b.*, u.name as user_name
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        WHERE b.event_id = %s
    """
    return execute_query(query, (event_id,))

def get_user_bookings(user_id: int) -> List[dict]:
    """Get all bookings for a specific user"""
    query = """
        SELECT b.*, e.name as event_name, e.date as event_date
        FROM bookings b
        JOIN events e ON b.event_id = e.id
        WHERE b.user_id = %s
    """
    return execute_query(query, (user_id,))

def get_booking_by_id(booking_id: int) -> dict:
    """Get a booking by its ID."""
    try:
        query = """
            SELECT b.*, u.name as user_name, e.name as event_name, e.date as event_date
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN events e ON b.event_id = e.id
            WHERE b.id = %s
        """
        result = execute_query(query, (booking_id,))
        if not result:
            raise NotFoundError(f"Booking with ID {booking_id} not found")
        return result[0]
    except Exception as e:
        raise DatabaseError(f"Failed to get booking: {str(e)}") 