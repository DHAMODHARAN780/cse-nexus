"""
Comprehensive Database Initialization Script for Production
This script creates all necessary database tables and seeds initial data
"""
from nexus import create_app
from extensions import db
from models.subject_model import Subject

app = create_app()

# All subjects for CSE curriculum (Semesters 1-8)
SUBJECTS_DATA = [
    # Semester 1
    {'code': 'CSBS101', 'title': 'Mathematics-I', 'semester': 1, 'credits': 4, 'type': 'theory', 'category': 'BS', 'image_url': 'images/subjects/mathematics.png'},
    {'code': 'CSBS102', 'title': 'Physics', 'semester': 1, 'credits': 3, 'type': 'theory', 'category': 'BS', 'image_url': 'images/subjects/math_theory.png'},
    {'code': 'CSES103', 'title': 'Basic Electronics Engineering', 'semester': 1, 'credits': 3, 'type': 'theory', 'category': 'ES', 'image_url': 'images/subjects/hardware.png'},
    {'code': 'CSBL101', 'title': 'Physics Lab', 'semester': 1, 'credits': 1, 'type': 'practical', 'category': 'BS', 'image_url': 'images/subjects/math_theory.png'},
    {'code': 'CSEL102', 'title': 'Basic Electronics Lab', 'semester': 1, 'credits': 1, 'type': 'practical', 'category': 'ES', 'image_url': 'images/subjects/hardware.png'},
    {'code': 'CSEL103', 'title': 'Engineering Graphics & Design Lab', 'semester': 1, 'credits': 2, 'type': 'practical', 'category': 'ES', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSHL104', 'title': 'Design Thinking', 'semester': 1, 'credits': 0, 'type': 'audit', 'category': 'HS', 'image_url': 'images/subjects/ai_data.png'},
    {'code': 'CSAU105', 'title': 'IDEA Lab Workshop', 'semester': 1, 'credits': 1, 'type': 'practical', 'category': 'AU', 'image_url': 'images/subjects/programming.png'},
    
    # Semester 2
    {'code': 'CSHS201', 'title': 'English', 'semester': 2, 'credits': 2, 'type': 'theory', 'category': 'HS', 'image_url': 'images/subjects/ai_data.png'},
    {'code': 'CSBS202', 'title': 'Mathematics-II', 'semester': 2, 'credits': 4, 'type': 'theory', 'category': 'BS', 'image_url': 'images/subjects/mathematics.png'},
    {'code': 'CSBS203', 'title': 'Chemistry', 'semester': 2, 'credits': 3, 'type': 'theory', 'category': 'BS', 'image_url': 'images/subjects/math_theory.png'},
    {'code': 'CSES204', 'title': 'Programming for Problem Solving', 'semester': 2, 'credits': 3, 'type': 'theory', 'category': 'ES', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSHS205', 'title': 'Universal Human Values-II', 'semester': 2, 'credits': 0, 'type': 'audit', 'category': 'HS', 'image_url': 'images/subjects/ai_data.png'},
    {'code': 'CSBL201', 'title': 'Chemistry Lab', 'semester': 2, 'credits': 1, 'type': 'practical', 'category': 'BS', 'image_url': 'images/subjects/math_theory.png'},
    {'code': 'CSEL202', 'title': 'Programming for Problem Solving Lab', 'semester': 2, 'credits': 2, 'type': 'practical', 'category': 'ES', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSEL203', 'title': 'Workshop/Manufacturing Lab', 'semester': 2, 'credits': 1, 'type': 'practical', 'category': 'ES', 'image_url': 'images/subjects/hardware.png'},
    {'code': 'CSAU204', 'title': 'Sports and Yoga', 'semester': 2, 'credits': 1, 'type': 'practical', 'category': 'AU', 'image_url': 'images/subjects/ai_data.png'},
    
    # Semester 3
    {'code': 'CSES301', 'title': 'Microprocessor and Microcontroller', 'semester': 3, 'credits': 3, 'type': 'theory', 'category': 'ES', 'image_url': 'images/subjects/hardware.png'},
    {'code': 'CSPC302', 'title': 'Data Structures and Algorithms', 'semester': 3, 'credits': 4, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSES303', 'title': 'Digital Electronics and Systems', 'semester': 3, 'credits': 3, 'type': 'theory', 'category': 'ES', 'image_url': 'images/subjects/hardware.png'},
    {'code': 'CSBS304', 'title': 'Mathematics-III', 'semester': 3, 'credits': 4, 'type': 'theory', 'category': 'BS', 'image_url': 'images/subjects/mathematics.png'},
    {'code': 'CSHS305', 'title': 'Principles of Management', 'semester': 3, 'credits': 3, 'type': 'theory', 'category': 'HS', 'image_url': 'images/subjects/ai_data.png'},
    {'code': 'CSEL301', 'title': 'Microprocessor and Microcontroller Lab', 'semester': 3, 'credits': 1, 'type': 'practical', 'category': 'ES', 'image_url': 'images/subjects/hardware.png'},
    {'code': 'CSPL302', 'title': 'Data Structure and Algorithms Lab', 'semester': 3, 'credits': 2, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSEL303', 'title': 'Digital Electronics and System Lab', 'semester': 3, 'credits': 1, 'type': 'practical', 'category': 'ES', 'image_url': 'images/subjects/hardware.png'},
    {'code': 'CSPL304', 'title': 'IT Workshop (SciLab/MATLAB)', 'semester': 3, 'credits': 1, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    
    # Semester 4
    {'code': 'CSPC401', 'title': 'Discrete Mathematics', 'semester': 4, 'credits': 4, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/mathematics.png'},
    {'code': 'CSPC402', 'title': 'Computer Organization & Architecture', 'semester': 4, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/hardware.png'},
    {'code': 'CSPC403', 'title': 'Design & Analysis of Algorithms', 'semester': 4, 'credits': 4, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPC404', 'title': 'Advanced Programming in JAVA', 'semester': 4, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSHS405', 'title': 'Organizational Behaviour', 'semester': 4, 'credits': 3, 'type': 'theory', 'category': 'HS', 'image_url': 'images/subjects/ai_data.png'},
    {'code': 'CSMC406', 'title': 'Environmental Sciences', 'semester': 4, 'credits': 0, 'type': 'audit', 'category': 'MC', 'image_url': 'images/subjects/ai_data.png'},
    {'code': 'CSPL401', 'title': 'Computer Organization & Architecture Lab', 'semester': 4, 'credits': 1, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/hardware.png'},
    {'code': 'CSPL402', 'title': 'Design & Analysis of Algorithms Lab', 'semester': 4, 'credits': 2, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPL403', 'title': 'JAVA Programming Lab', 'semester': 4, 'credits': 2, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    
    # Semester 5
    {'code': 'CSPC501', 'title': 'Computer Networks', 'semester': 5, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/networking.png'},
    {'code': 'CSPC502', 'title': 'Database Systems', 'semester': 5, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPC503', 'title': 'Theory of Computation', 'semester': 5, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/mathematics.png'},
    {'code': 'CSPC504', 'title': 'Operating System', 'semester': 5, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPE_V', 'title': 'Professional Elective-I', 'semester': 5, 'credits': 3, 'type': 'elective', 'category': 'PE', 'image_url': 'images/subjects/ai_ml.png'},
    {'code': 'CSMC505', 'title': 'Constitution of India', 'semester': 5, 'credits': 0, 'type': 'audit', 'category': 'MC', 'image_url': 'images/subjects/ai_data.png'},
    {'code': 'CSPL501', 'title': 'Computer Networks Lab', 'semester': 5, 'credits': 1, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/networking.png'},
    {'code': 'CSPL502', 'title': 'Database Systems Lab', 'semester': 5, 'credits': 2, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPL503', 'title': 'Operating Systems Lab', 'semester': 5, 'credits': 2, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    
    # Semester 6
    {'code': 'CSPC601', 'title': 'Web Technology', 'semester': 6, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPC602', 'title': 'Compiler Design', 'semester': 6, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPC603', 'title': 'Distributed Computing System', 'semester': 6, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/networking.png'},
    {'code': 'CSPC604', 'title': 'Artificial Intelligence and Machine Learning', 'semester': 6, 'credits': 4, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/ai_ml.png'},
    {'code': 'CSPE_VI', 'title': 'Professional Elective-II', 'semester': 6, 'credits': 3, 'type': 'elective', 'category': 'PE', 'image_url': 'images/subjects/ai_ml.png'},
    {'code': 'CSPL601', 'title': 'Web Technology Lab', 'semester': 6, 'credits': 2, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPL602', 'title': 'Compiler Design Lab', 'semester': 6, 'credits': 2, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPROJ603', 'title': 'Mini Project', 'semester': 6, 'credits': 2, 'type': 'practical', 'category': 'PROJ', 'image_url': 'images/subjects/programming.png'},
    
    # Semester 7
    {'code': 'CSPC701', 'title': 'Cyber Security', 'semester': 7, 'credits': 3, 'type': 'theory', 'category': 'PC', 'image_url': 'images/subjects/networking.png'},
    {'code': 'CSBS702', 'title': 'Biology', 'semester': 7, 'credits': 3, 'type': 'theory', 'category': 'BS', 'image_url': 'images/subjects/ai_data.png'},
    {'code': 'CSPE_VII', 'title': 'Professional Elective-III', 'semester': 7, 'credits': 3, 'type': 'elective', 'category': 'PE', 'image_url': 'images/subjects/ai_ml.png'},
    {'code': 'CSOE_VII', 'title': 'Open Elective-I', 'semester': 7, 'credits': 3, 'type': 'elective', 'category': 'OE', 'image_url': 'images/subjects/ai_ml.png'},
    {'code': 'CSPL701', 'title': 'Cyber Security Lab', 'semester': 7, 'credits': 2, 'type': 'practical', 'category': 'PC', 'image_url': 'images/subjects/networking.png'},
    {'code': 'CSPROJ702', 'title': 'Seminar', 'semester': 7, 'credits': 1, 'type': 'practical', 'category': 'PROJ', 'image_url': 'images/subjects/ai_data.png'},
    {'code': 'CSPROJ703', 'title': 'Capstone Project-I', 'semester': 7, 'credits': 4, 'type': 'practical', 'category': 'PROJ', 'image_url': 'images/subjects/programming.png'},
    
    # Semester 8
    {'code': 'CSPE_VIII', 'title': 'Professional Elective-IV', 'semester': 8, 'credits': 3, 'type': 'elective', 'category': 'PE', 'image_url': 'images/subjects/ai_ml.png'},
    {'code': 'CSOE_VIII_A', 'title': 'Open Elective-II', 'semester': 8, 'credits': 3, 'type': 'elective', 'category': 'OE', 'image_url': 'images/subjects/ai_ml.png'},
    {'code': 'CSOE_VIII_B', 'title': 'Open Elective-III', 'semester': 8, 'credits': 3, 'type': 'elective', 'category': 'OE', 'image_url': 'images/subjects/ai_ml.png'},
    {'code': 'CSPROJ801', 'title': 'Capstone Project-II', 'semester': 8, 'credits': 10, 'type': 'practical', 'category': 'PROJ', 'image_url': 'images/subjects/programming.png'},
    {'code': 'CSPROJ802', 'title': 'Internship', 'semester': 8, 'credits': 2, 'type': 'practical', 'category': 'PROJ', 'image_url': 'images/subjects/ai_data.png'},
]

def init_db():
    """Initialize database with all tables and seed data"""
    with app.app_context():
        print("Creating all database tables...")
        db.create_all()
        print("✓ Tables created successfully!")
        
        # Check if subjects already exist
        existing_count = Subject.query.count()
        if existing_count > 0:
            print(f"⚠ Database already has {existing_count} subjects. Skipping seed.")
            return
        
        print(f"\nAdding {len(SUBJECTS_DATA)} subjects to database...")
        
        for subject_data in SUBJECTS_DATA:
            subject = Subject(**subject_data)
            db.session.add(subject)
        
        db.session.commit()
        print(f"✓ Successfully added {len(SUBJECTS_DATA)} subjects!")
        
        # Verify
        total = Subject.query.count()
        print(f"\n✓ Database now has {total} subjects total")
        
        # Show summary by semester
        print("\nSubjects by Semester:")
        for sem in range(1, 9):
            count = Subject.query.filter_by(semester=sem).count()
            print(f"  Semester {sem}: {count} subjects")

if __name__ == '__main__':
    init_db()
