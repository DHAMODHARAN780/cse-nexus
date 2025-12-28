from nexus import create_app
from extensions import db
from models.user_model import User
from models.subject_model import Subject

app = create_app()

with app.app_context():
    # Check all users and their semesters
    users = User.query.all()
    
    print("=" * 60)
    print("USER ACCOUNTS AND THEIR SEMESTERS")
    print("=" * 60)
    
    for user in users:
        print(f"\nName: {user.name}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Year: {user.year}")
        print(f"Semester: {user.semester}")
        print(f"Reg No: {user.reg_no}")
        
        if user.role == 'student' and user.semester:
            # Count subjects for this semester
            subject_count = Subject.query.filter_by(semester=user.semester).count()
            print(f"Subjects available for Semester {user.semester}: {subject_count}")
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("SUBJECTS BY SEMESTER")
    print("=" * 60)
    
    for sem in range(1, 9):
        subjects = Subject.query.filter_by(semester=sem).all()
        print(f"\nSemester {sem}: {len(subjects)} subjects")
        for sub in subjects[:3]:  # Show first 3
            print(f"  - {sub.code}: {sub.title}")
        if len(subjects) > 3:
            print(f"  ... and {len(subjects) - 3} more")
