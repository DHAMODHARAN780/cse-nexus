import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extensions import db

from datetime import datetime

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False) # 'material', 'video'
    filepath = db.Column(db.String(300), nullable=False)
    
    subject = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.Integer, nullable=False) # 1-5
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    uploader = db.relationship('User', backref='uploads')

    def __repr__(self):
        return f'<Content {self.title}>'
