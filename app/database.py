import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

# Load environment variables
load_dotenv()

# Database configuration with default values
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "ticket_booking")
}

class DatabaseError(Exception):
    """Base exception for database operations"""
    pass

class DuplicateUserError(DatabaseError):
    """Raised when attempting to create a user with an existing email"""
    pass

class DuplicateBookingError(DatabaseError):
    """Raised when attempting to create a duplicate booking"""
    pass

class NotFoundError(DatabaseError):
    """Raised when a requested resource is not found"""
    pass

def get_connection(database: Optional[str] = None) -> mysql.connector.MySQLConnection:
    """
    Get a database connection.
    If database is None, uses the database from DB_CONFIG.
    """
    try:
        config = DB_CONFIG.copy()
        if database is not None:
            config["database"] = database
        return mysql.connector.connect(**config)
    except Error as e:
        raise DatabaseError(f"Failed to connect to database: {str(e)}")

def execute_query(query: str, params: tuple = None, fetch: bool = True) -> List[Dict[str, Any]]:
    """
    Execute a query and optionally fetch results.
    Returns the results if fetch=True, otherwise returns the lastrowid.
    """
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            return result if result else []
        else:
            connection.commit()
            return cursor.lastrowid
            
    except Error as e:
        if connection:
            connection.rollback()
        if e.errno == 1062:  # Duplicate entry
            if "users.email" in str(e):
                raise DuplicateUserError("Email already exists")
            elif "bookings" in str(e):
                raise DuplicateBookingError("User has already booked this event")
        raise DatabaseError(f"Query execution failed: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# def execute_many_queries(queries: List[str], database: Optional[str] = None) -> None:
#     """
#     Execute multiple queries in a single transaction.
#     Useful for initialization scripts.
#     """
#     connection = None
#     cursor = None
#     try:
#         connection = get_connection(database)
#         cursor = connection.cursor()
        
#         for query in queries:
#             if query.strip():
#                 cursor.execute(query)
                
#         connection.commit()
#     except Error as e:
#         if connection:
#             connection.rollback()
#         raise DatabaseError(f"Failed to execute queries: {str(e)}")
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close() 