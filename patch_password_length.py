from nexus import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

def patch_password_length():
    with app.app_context():
        engine = db.engine
        # Mask password in DB URL for printing
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"Connecting to database...")
        
        # Check dialect
        dialect = engine.dialect.name
        print(f"Database dialect: {dialect}")
        
        if dialect == 'postgresql':
            print("Detected PostgreSQL. Attempting to alter column length...")
            try:
                with engine.connect() as conn:
                    # Using "user" with double quotes because user is a reserved word
                    conn.execute(text('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(256);'))
                    conn.commit()
                print("Successfully altered password_hash length to 256.")
            except Exception as e:
                print(f"Error altering table: {e}")
        elif dialect == 'sqlite':
            print("Detected SQLite. SQLite does not support simple ALTER COLUMN.")
            print("However, SQLite is dynamically typed and usually does not enforce length limits on VARCHAR.")
            print("No patch needed for SQLite local development typically.")
        else:
            print(f"Unknown dialect: {dialect}. Please manually update the table if needed.")

if __name__ == "__main__":
    patch_password_length()
