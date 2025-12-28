import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from extensions import db

from datetime import datetime

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True) # Main Subject / Summary
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='notice') # 'notice', 'exam', 'upload', 'event'
    date = db.Column(db.DateTime, default=datetime.utcnow)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(500), nullable=True) # Optional attachment
    
    poster = db.relationship('User', backref='announcements')

    def __repr__(self):
        return f'<Announcement {self.id}>'
