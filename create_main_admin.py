
import sqlite3
import os
from werkzeug.security import generate_password_hash

def create_main_admin():
    db_path = 'instance/database.db'
    if not os.path.exists(db_path):
        db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    name = "Main Admin"
    email = "admin@csenexus.com"
    password = "adminpassword123"
    role = "main_admin"
    password_hash = generate_password_hash(password)
    
    try:
        cursor.execute("INSERT INTO user (name, email, password_hash, role, status) VALUES (?, ?, ?, ?, ?)", 
                       (name, email, password_hash, role, 'active'))
        conn.commit()
        print(f"Main Admin created successfully!")
        print(f"Email: {email}")
        print(f"Password: {password}")
    except sqlite3.IntegrityError:
        print(f"User with email {email} already exists. Updating role to main_admin...")
        cursor.execute("UPDATE user SET role = ?, password_hash = ? WHERE email = ?", (role, password_hash, email))
        conn.commit()
        print("User updated to Main Admin.")
    except Exception as e:
        print(f"Error: {e}")

    conn.close()

if __name__ == "__main__":
    create_main_admin()
