import sqlite3
import os

def patch_otp_columns():
    db_path = 'instance/database.db'
    if not os.path.exists(db_path):
        db_path = 'database.db'
    
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Adding otp_code column...")
        cursor.execute("ALTER TABLE user ADD COLUMN otp_code TEXT")
        print("otp_code added successfully.")
    except sqlite3.OperationalError:
        print("otp_code column already exists or table doesn't exist.")

    try:
        print("Adding otp_expiry column...")
        cursor.execute("ALTER TABLE user ADD COLUMN otp_expiry DATETIME")
        print("otp_expiry added successfully.")
    except sqlite3.OperationalError:
        print("otp_expiry column already exists.")
        
    conn.commit()
    conn.close()
    print("Database patching complete!")

if __name__ == "__main__":
    patch_otp_columns()
