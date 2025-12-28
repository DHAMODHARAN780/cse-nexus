from nexus import create_app
from extensions import db
import sqlite3
import os

app = create_app()
with app.app_context():
    # 1. Create new tables (like Timetable)
    db.create_all()
    print("New tables created (if any).")
    
    # 2. Add missing columns to existing tables using raw SQL
    # The database is likely in the 'instance' folder
    db_path = os.path.join(app.root_path, 'instance', 'database.db')
    if not os.path.exists(db_path):
        db_path = 'database.db' # Fallback to root
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add file_path to announcement
        try:
            cursor.execute('ALTER TABLE announcement ADD COLUMN file_path VARCHAR(500)')
            print("Successfully added 'file_path' to 'announcement' table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("'file_path' already exists in 'announcement' table.")
            else:
                print(f"Error updating 'announcement': {e}")

        # Add file_path to achievement
        try:
            cursor.execute('ALTER TABLE achievement ADD COLUMN file_path VARCHAR(500)')
            print("Successfully added 'file_path' to 'achievement' table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("'file_path' already exists in 'achievement' table.")
            else:
                print(f"Error updating 'achievement': {e}")
                
        conn.commit()
        conn.close()
    else:
        print(f"Database file not found at {db_path}. Running db.create_all() was sufficient.")

    print("Database maintenance completed.")
