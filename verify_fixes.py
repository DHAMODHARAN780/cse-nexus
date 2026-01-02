
import sqlite3
import os

def verify_fixes():
    db_path = 'instance/database.db'
    if not os.path.exists(db_path):
        db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    print(f"Verifying fixes in database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verify paths don't start with static/ anymore
    tables_cols = {
        'achievement': ['image_url', 'file_path'],
        'announcement': ['file_path'],
        'timetable': ['file_path'],
        'content': ['filepath']
    }
    
    all_good = True
    for table, cols in tables_cols.items():
        for col in cols:
            cursor.execute(f"SELECT {col} FROM {table} WHERE {col} LIKE 'static/%'")
            bad_rows = cursor.fetchall()
            if bad_rows:
                print(f"FAILURE: Table {table} still has {len(bad_rows)} records in {col} starting with 'static/'")
                all_good = False
            else:
                print(f"SUCCESS: Table {table} column {col} is clean.")
    
    if all_good:
        print("\nOVERALL PATH VERIFICATION: PASSED")
    else:
        print("\nOVERALL PATH VERIFICATION: FAILED")

    conn.close()

if __name__ == "__main__":
    verify_fixes()
