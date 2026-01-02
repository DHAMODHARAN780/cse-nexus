
import sqlite3
import os

def check_db():
    db_path = 'instance/database.db'
    if not os.path.exists(db_path):
        db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    print(f"Checking database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check user table columns
    try:
        cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"User table columns: {columns}")
        
        has_otp_code = 'otp_code' in columns
        has_otp_expiry = 'otp_expiry' in columns
        print(f"Has otp_code: {has_otp_code}")
        print(f"Has otp_expiry: {has_otp_expiry}")
        
    except Exception as e:
        print(f"Error checking user table: {e}")

    # Check some data in Achievement to see paths
    try:
        cursor.execute("SELECT image_url, file_path FROM achievement LIMIT 3")
        rows = cursor.fetchall()
        print("Achievement samples:")
        for row in rows:
            print(f"image_url: {row[0]}, file_path: {row[1]}")
    except Exception as e:
        print(f"Error checking achievement table: {e}")

    conn.close()

if __name__ == "__main__":
    check_db()
