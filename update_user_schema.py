from extensions import db
from sqlalchemy import text

def update_user_schema():
    with db.engine.connect() as conn:
        try:
            conn.execute(text("""
                ALTER TABLE "user"
                ADD COLUMN IF NOT EXISTS designation VARCHAR(50)
            """))
            conn.commit()
            print("✓ Added designation column to user table")
        except Exception as e:
            print(f"Error updating user schema: {e}")
            # For PostgreSQL, IF NOT EXISTS is supported in newer versions, 
            # but if it fails we log it.
            
if __name__ == "__main__":
    from nexus import create_app
    app = create_app()
    with app.app_context():
        update_user_schema()
