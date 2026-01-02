from extensions import db
from sqlalchemy import text

def update_production_schema():
    """
    Ensures all expected columns across all tables exist in PostgreSQL.
    This script is safe for Render Free Tier (idempotent).
    """
    # Dictionary of table_name: List of (column_name, column_type, default_value)
    schema_patches = {
        "user": [
            ("designation", "VARCHAR(50)", None),
            ("otp_code", "VARCHAR(6)", None),
            ("otp_expiry", "TIMESTAMP", None),
            ("status", "VARCHAR(20)", "'active'"),
            ("reg_no", "VARCHAR(30)", None),
            ("year", "INTEGER", None),
            ("semester", "INTEGER", None),
        ],
        "login_log": [
            ("ip_address", "VARCHAR(50)", None),
            ("user_agent", "VARCHAR(255)", None),
        ],
        "announcement": [
            ("title", "VARCHAR(200)", None),
        ],
        "subject": [
            ("image_url", "VARCHAR(300)", None),
        ]
    }
    
    with db.engine.connect() as conn:
        print("Starting Production Schema Audit...")
        for table, columns in schema_patches.items():
            for col_name, col_type, default in columns:
                try:
                    # Double quotes handle reserved names like "user"
                    sql = f'ALTER TABLE "{table}" ADD COLUMN IF NOT EXISTS {col_name} {col_type}'
                    if default:
                        sql += f" DEFAULT {default}"
                    
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"✓ Table '{table}': Ensured column '{col_name}' exists.")
                except Exception as e:
                    print(f"⚠ Table '{table}', Column '{col_name}': {e}")
        print("Schema Audit Complete.")

if __name__ == "__main__":
    from nexus import create_app
    app = create_app()
    with app.app_context():
        update_production_schema()
