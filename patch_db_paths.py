
```python
import sqlite3
import os

def patch_db_paths():
    db_path = 'instance/database.db'
    if not os.path.exists(db_path):
        # - [x] Create templates for Main Admin Dashboard <!-- id: 11 -->
        # - [x] Register `admin_bp` in `nexus.py` <!-- id: 12 -->
        # - [x] Implement Monitoring for Faculties and Students <!-- id: 13 -->
        # - [x] Sort students alphabetically in Main Admin view <!-- id: 15 -->
        # - [x] Implement Quick Filter logic for student monitoring <!-- id: 16 -->
        # - [/] Move Security Code settings to Main Admin only <!-- id: 17 -->
        # - [/] Implement Main Admin registration with master key <!-- id: 18 -->
        # - [ ] Verify Main Admin functionality <!-- id: 14 -->
        db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    print(f"Patching database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tables_cols = {
        'achievement': ['image_url', 'file_path'],
        'announcement': ['file_path'],
        'timetable': ['file_path'],
        'content': ['filepath']
    }
    
    for table, cols in tables_cols.items():
        for col in cols:
            print(f"Processing {table}.{col}...")
            cursor.execute(f"SELECT id, {col} FROM {table} WHERE {col} IS NOT NULL")
            rows = cursor.fetchall()
            for row_id, path in rows:
                if path and path.startswith('static/'):
                    new_path = path.replace('static/', '', 1)
                    print(f"Updating {table} ID {row_id}: {path} -> {new_path}")
                    cursor.execute(f"UPDATE {table} SET {col} = ? WHERE id = ?", (new_path, row_id))
    
    conn.commit()
    conn.close()
    print("Database path patching complete!")

if __name__ == "__main__":
    patch_db_paths()
