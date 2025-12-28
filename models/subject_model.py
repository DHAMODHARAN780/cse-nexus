from extensions import db
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False) # 'theory', 'practical', 'audit', 'elective'
    category = db.Column(db.String(50), nullable=True) # 'HSM', 'BSC', 'ESC', 'PCC', etc.
    image_url = db.Column(db.String(300), nullable=True) # Thematic background image
    lecture = db.Column(db.Integer, default=0)
    tutorial = db.Column(db.Integer, default=0)
    practical = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Subject {self.code}: {self.title}>'
