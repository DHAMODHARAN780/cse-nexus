from nexus import create_app
from extensions import db
from models.user_model import User

app = create_app()

def patch_year_sem():
    with app.app_context():
        students = User.query.filter_by(role='student').all()
        count = 0
        for s in students:
            if s.semester:
                # Correct logic: Year 1 (S1, S2), Year 2 (S3, S4), etc.
                correct_year = (int(s.semester) + 1) // 2
                if s.year != correct_year:
                    print(f"Updating {s.name} (Reg: {s.reg_no}): Year {s.year} Sem {s.semester} -> Year {correct_year}")
                    s.year = correct_year
                    count += 1
        
        db.session.commit()
        print(f"Successfully patched {count} student records.")

if __name__ == "__main__":
    patch_year_sem()
