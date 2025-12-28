"""
Comprehensive Database Initialization Script for Production
Safe for Render Free Tier (idempotent)
"""

from extensions import db
from models.subject_model import Subject

# All subjects for CSE curriculum (Semesters 1-8)
SUBJECTS_DATA = [
    # (UNCHANGED — keep all your 64 subjects exactly as you wrote them)
    # ... no modification needed here ...
]

def init_db():
    """Initialize database tables and seed subjects (runs only once)"""
    print("Initializing production database...")

    # Create tables if not exist
    db.create_all()

    existing_count = Subject.query.count()
    if existing_count > 0:
        print(f"⚠ Subjects already exist ({existing_count}). Skipping initialization.")
        return

    print(f"Adding {len(SUBJECTS_DATA)} subjects...")

    for data in SUBJECTS_DATA:
        db.session.add(Subject(**data))

    db.session.commit()

    print(f"✓ Successfully added {len(SUBJECTS_DATA)} subjects.")

    # Summary
    for sem in range(1, 9):
        count = Subject.query.filter_by(semester=sem).count()
        print(f"Semester {sem}: {count} subjects")
