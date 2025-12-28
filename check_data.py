from nexus import create_app
from extensions import db
from models.user_model import User
from models.timetable_model import Timetable

app = create_app()
with app.app_context():
    print("--- Users ---")
    users = User.query.all()
    for u in users:
        print(f"ID: {u.id}, Name: {u.name}, Role: {u.role}, Sem: {u.semester} ({type(u.semester)}), Year: {u.year}")

    print("\n--- Timetables ---")
    timetables = Timetable.query.all()
    if not timetables:
        print("No timetables found in DB.")
    for t in timetables:
        print(f"ID: {t.id}, Title: {t.title}, Sem: {t.semester} ({type(t.semester)}), Year: {t.year}")
