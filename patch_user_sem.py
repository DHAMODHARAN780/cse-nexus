from nexus import create_app
from extensions import db
from models.user_model import User

app = create_app()
with app.app_context():
    # Update Dhamodharan (ID: 1) to Semester 4 to match the uploaded timetable
    user = User.query.get(1)
    if user:
        user.semester = 4
        db.session.commit()
        print(f"Updated user {user.name} to Semester {user.semester}")
    else:
        print("User not found.")
