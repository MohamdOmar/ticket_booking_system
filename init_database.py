import mysql.connector
from mysql.connector import Error
from app.database import execute_many_queries, DatabaseError

def init_database():
    try:
        # First, create a connection without selecting a database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        
        # Drop and create the database
        cursor.execute("DROP DATABASE IF EXISTS ticket_booking")
        cursor.execute("CREATE DATABASE ticket_booking")
        cursor.close()
        conn.close()

        # Now read and execute the SQL script
        with open('init_db.sql', 'r') as file:
            sql_commands = file.read()
            
        # Split and execute multiple commands
        queries = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
        execute_many_queries(queries, "ticket_booking")
        print("Database and tables created successfully!")

    except Error as e:
        print(f"MySQL Error: {e}")
    except DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    init_database() 