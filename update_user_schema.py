from extensions import db
from sqlalchemy import text

def update_user_schema():
    """
    Ensures all expected columns for the 'user' table exist in PostgreSQL.
    This script is safe for Render Free Tier (idempotent).
    """
    # List of (column_name, column_type, default_value)
    columns_to_ensure = [
        ("designation", "VARCHAR(50)", None),
        ("otp_code", "VARCHAR(6)", None),
        ("otp_expiry", "TIMESTAMP", None),
        ("status", "VARCHAR(20)", "'active'"),
        ("reg_no", "VARCHAR(30)", None),
        ("year", "INTEGER", None),
        ("semester", "INTEGER", None),
    ]
    
    with db.engine.connect() as conn:
        for col_name, col_type, default in columns_to_ensure:
            try:
                sql = f'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS {col_name} {col_type}'
                if default:
                    sql += f" DEFAULT {default}"
                
                conn.execute(text(sql))
                conn.commit()
                print(f"✓ Ensured column '{col_name}' exists in user table")
            except Exception as e:
                # Often occurs if column already exists (in older PG versions without IF NOT EXISTS)
                # or if there's a constraint violation.
                print(f"⚠ Note for column '{col_name}': {e}")
                
if __name__ == "__main__":
    from nexus import create_app
    app = create_app()
    with app.app_context():
        update_user_schema()
