import sqlite3
import os

def patch_announcement():
    # Detect DB path
    db_paths = [
        os.path.join('instance', 'database.db'),
        'database.db'
    ]
    
    db_path = None
    for p in db_paths:
        if os.path.exists(p):
            db_path = p
            break
            
    if not db_path:
        print("Database not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print(f"Patching database at {db_path}...")
        # Add title to announcement if it doesn't exist
        cursor.execute("ALTER TABLE announcement ADD COLUMN title VARCHAR(200)")
        print("Added 'title' column to announcement table.")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e).lower() or 'already exists' in str(e).lower():
            print("Column 'title' already exists in announcement table.")
        else:
            print(f"Error: {e}")

    conn.commit()
    conn.close()
    print("Patch complete.")

if __name__ == "__main__":
    patch_announcement()
