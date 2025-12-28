import sys
import os
sys.path.append(os.getcwd())
from nexus import create_app
from models.subject_model import Subject

app = create_app()
with app.app_context():
    subjects = Subject.query.all()
    categories = list(set([s.category for s in subjects if s.category]))
    print("CATEGORIES:", categories)
    print("---")
    for s in subjects:
        print(f"[{s.category}] {s.code}: {s.title}")
