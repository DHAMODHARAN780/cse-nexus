import sqlite3
import os

def update_schema():
    db_path = 'instance/database.db'
    if not os.path.exists(db_path):
        db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE user ADD COLUMN designation VARCHAR(100)")
        print("Successfully added designation column to user table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Column 'designation' already exists.")
        else:
            print(f"Error: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_schema()
