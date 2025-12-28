from nexus import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    db.session.execute(
        text('ALTER TABLE "user" ALTER COLUMN password_hash TYPE TEXT')
    )
    db.session.commit()
    print("password_hash column updated to TEXT")
