import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extensions import db, login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text)
    role = db.Column(db.String(20), nullable=False) # 'student', 'admin', 'main_admin'
    designation = db.Column(db.String(100), nullable=True) # 'HOD', 'Principal', etc.
    
    # Student specific
    reg_no = db.Column(db.String(30), unique=True, nullable=True)
    year = db.Column(db.Integer, nullable=True)     # 1, 2, 3, 4
    semester = db.Column(db.Integer, nullable=True) # 1-8
    status = db.Column(db.String(20), default='active') # 'active', 'blacklisted'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # OTP for password reset
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_main_admin(self):
        return self.role == 'main_admin'

    def get_reset_token(self):
        from itsdangerous import URLSafeTimedSerializer as Serializer
        from flask import current_app
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        from itsdangerous import URLSafeTimedSerializer as Serializer
        from flask import current_app
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def generate_otp(self):
        import random
        from datetime import datetime, timedelta
        self.otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
        return self.otp_code

    def verify_otp_code(self, otp):
        from datetime import datetime
        if self.otp_code == otp and self.otp_expiry > datetime.utcnow():
            return True
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
