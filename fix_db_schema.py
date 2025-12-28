import sqlite3
import os

def add_status_column():
    possible_paths = ['instance/database.db', 'database.db']
    for found_path in possible_paths:
        if not os.path.exists(found_path):
            print(f"File not found: {found_path}")
            continue

        print(f"Checking {found_path}...")
        try:
            conn = sqlite3.connect(found_path)
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
            if not cursor.fetchone():
                print(f"Table 'user' does not exist in {found_path}. Skipping.")
                conn.close()
                continue
                
            cursor.execute("ALTER TABLE user ADD COLUMN status VARCHAR(20) DEFAULT 'active'")
            conn.commit()
            conn.close()
            print(f"Column 'status' added successfully to {found_path}.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"Column 'status' already exists in {found_path}.")
            else:
                print(f"Operational Error in {found_path}: {e}")
        except Exception as e:
            print(f"An error occurred in {found_path}: {e}")

if __name__ == "__main__":
    add_status_column()
