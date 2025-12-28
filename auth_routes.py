import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user_model import User
from models.login_log_model import LoginLog

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('faculty.dashboard'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if user.status == 'blacklisted':
                flash('Your account is blacklisted. Please contact administration.', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user)
            
            # Log the login
            log = LoginLog(user_id=user.id)
            db.session.add(log)
            db.session.commit()
            
            if user.role == 'admin':
                return redirect(url_for('faculty.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    from models.announcement_model import Announcement
    announcements = Announcement.query.order_by(Announcement.date.desc()).limit(3).all()
    return render_template('auth/login.html', announcements=announcements)

@auth_bp.route('/register')
def register():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('faculty.dashboard'))
        return redirect(url_for('student.dashboard'))
    return render_template('auth/register.html')

@auth_bp.route('/register_faculty')
def register_faculty():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('faculty.dashboard'))
        return redirect(url_for('student.dashboard'))
    return render_template('auth/faculty_registration.html')

@auth_bp.route('/register_action', methods=['POST'])
def register_action():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role') # 'student' or 'admin'
    
    reg_no = request.form.get('reg_no')
    
    # Validation
    user = User.query.filter_by(email=email).first()
    if user:
        if user.status == 'blacklisted':
            flash('This account is blacklisted and cannot be recreated.', 'danger')
        else:
            flash('Email already registered', 'warning')
        if role == 'admin':
            return redirect(url_for('auth.register_faculty'))
        return redirect(url_for('auth.register'))

    if role == 'student' and reg_no:
        existing_reg = User.query.filter_by(reg_no=reg_no).first()
        if existing_reg:
            if existing_reg.status == 'blacklisted':
                flash('This register number is blacklisted.', 'danger')
            else:
                flash('Register number already exists', 'warning')
            return redirect(url_for('auth.register'))

    new_user = User(name=name, email=email, role=role, reg_no=reg_no)
    new_user.set_password(password)

    if role == 'admin':
        from flask import current_app
        from models.settings_model import SystemSetting
        
        access_code = request.form.get('access_code')
        # Check DB first, fallback to config if not set
        db_code = SystemSetting.get_setting('faculty_access_code')
        required_code = db_code if db_code else current_app.config.get('FACULTY_ACCESS_CODE')
        
        if access_code != required_code:
            flash('Invalid Security Access Code. Registration denied.', 'danger')
            return redirect(url_for('auth.register_faculty'))

    if role == 'student':
        semester = int(request.form.get('semester'))
        new_user.semester = semester
        # Auto-calculate year based on semester
        new_user.year = (semester + 1) // 2
    
    db.session.add(new_user)
    db.session.commit()
    
    flash('Account created! You can now login.', 'success')
    return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            otp = user.generate_otp()
            db.session.commit()
            send_otp_email(user, otp)
            from flask import session
            session['reset_email'] = email
            flash('Success! A 6-digit verification code is on its way.', 'info')
            return redirect(url_for('auth.verify_otp'))
        else:
            flash('There is no account with that email. You must register first.', 'warning')
    return render_template('auth/forgot_password.html')

@auth_bp.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    from flask import session
    email = session.get('reset_email')
    if not email:
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        otp = request.form.get('otp')
        user = User.query.filter_by(email=email).first()
        if user and user.verify_otp_code(otp):
            session['otp_verified'] = True
            return redirect(url_for('auth.reset_password'))
        else:
            flash('Invalid or expired OTP. Please try again.', 'danger')
            
    return render_template('auth/verify_otp.html', email=email)

def send_otp_email(user, otp):
    from flask import current_app, flash
    from flask_mail import Message
    from extensions import mail
    
    msg = Message('Your Password Reset OTP - CSE Nexus',
                  sender='noreply@csenexus.com',
                  recipients=[user.email])
    msg.body = f'''Your password reset OTP is: {otp}

This code will expire in 10 minutes. 

If you did not make this request then simply ignore this email and no changes will be made.
'''
    
    # Check if mail is configured
    mail_user = current_app.config.get('MAIL_USERNAME')
    if not mail_user or 'your-email' in mail_user:
        print("\n" + "="*50)
        print(f"DEVELOPER MODE: OTP for {user.email} is: {otp}")
        print("="*50 + "\n")
        flash(f"YOUR OTP FOR RESETTING PASSWORD IS: {otp}", "warning")
        return

    print(f"Attempting to send OTP email to {user.email}")
    try:
        mail.send(msg)
        print("OTP email sent successfully!")
    except Exception as e:
        print(f"CRITICAL: Error sending email: {e}")
        print(f"FALLBACK: OTP for {user.email} is: {otp}")
        flash(f"[Dev Fallback] OTP for testing: {otp}", "warning")
        import traceback
        traceback.print_exc()

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    from flask import session
    if not session.get('otp_verified') or not session.get('reset_email'):
        flash('Please verify your OTP first.', 'warning')
        return redirect(url_for('auth.forgot_password'))
    
    email = session.get('reset_email')
    user = User.query.filter_by(email=email).first()
    
    if user is None:
        flash('Invalid request.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        user.set_password(password)
        # Clear OTP and session after success
        user.otp_code = None
        user.otp_expiry = None
        db.session.commit()
        
        session.pop('reset_email', None)
        session.pop('otp_verified', None)
        
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html')
