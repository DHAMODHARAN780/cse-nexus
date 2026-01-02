
import sqlite3
import os

def update_login_log_schema():
    db_path = 'instance/database.db'
    if not os.path.exists(db_path):
        db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    print(f"Updating schema at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE login_log ADD COLUMN ip_address VARCHAR(50)")
        print("Added ip_address column to login_log.")
    except sqlite3.OperationalError as e:
        print(f"Column ip_address might already exist: {e}")

    try:
        cursor.execute("ALTER TABLE login_log ADD COLUMN user_agent VARCHAR(255)")
        print("Added user_agent column to login_log.")
    except sqlite3.OperationalError as e:
        print(f"Column user_agent might already exist: {e}")
    
    conn.commit()
    conn.close()
    print("Schema update complete!")

if __name__ == "__main__":
    update_login_log_schema()
