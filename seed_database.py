from datetime import datetime, timedelta
from app import db_utils

def seed_database():
    try:
        # Create dummy users
        users = [
            ("John Doe", "john@example.com"),
            ("Jane Smith", "jane@example.com"),
            ("Bob Johnson", "bob@example.com"),
            ("Alice Brown", "alice@example.com"),
            ("Charlie Wilson", "charlie@example.com")
        ]
        
        print("Creating users...")
        for name, email in users:
            db_utils.create_user(name, email)
        print("Users created successfully!")

        # Create dummy events
        events = [
            ("Rock Concert", datetime.now() + timedelta(days=7), 100),
            ("Jazz Festival", datetime.now() + timedelta(days=14), 200),
            ("Comedy Show", datetime.now() + timedelta(days=21), 50),
            ("Theater Play", datetime.now() + timedelta(days=28), 75),
            ("Dance Performance", datetime.now() + timedelta(days=35), 150)
        ]
        
        print("Creating events...")
        for name, date, capacity in events:
            db_utils.create_event(name, date, capacity)
        print("Events created successfully!")

        # Create dummy bookings
        bookings = [
            (1, 1),  # John books Rock Concert
            (2, 1),  # Jane books Rock Concert
            (3, 2),  # Bob books Jazz Festival
            (4, 2),  # Alice books Jazz Festival
            (5, 3),  # Charlie books Comedy Show
            (1, 4),  # John books Theater Play
            (2, 5),  # Jane books Dance Performance
            (3, 3),  # Bob books Comedy Show
            (4, 4),  # Alice books Theater Play
            (5, 5)   # Charlie books Dance Performance
        ]
        
        print("Creating bookings...")
        for user_id, event_id in bookings:
            db_utils.create_booking(user_id, event_id)
        print("Bookings created successfully!")

        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")

if __name__ == "__main__":
    seed_database() 