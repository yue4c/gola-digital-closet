import sqlite3


def create_database():
    # Connect to database
    connection = sqlite3.connect("gola.db")

    # Create cursor
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Save changes
    connection.commit()

    # Close database
    connection.close()


create_database()