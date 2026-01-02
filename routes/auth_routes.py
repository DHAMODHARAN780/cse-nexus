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
        if current_user.role == 'main_admin':
            return redirect(url_for('admin.dashboard'))
        if current_user.role == 'admin':
            return redirect(url_for('faculty.dashboard'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember')) # Added remember me functionality
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if user.status == 'blacklisted':
                flash('Your account has been blacklisted. Please contact administration.', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user, remember=remember)
            
            # Log the login
            log = LoginLog(user_id=user.id, ip_address=request.remote_addr, user_agent=request.user_agent.string)
            db.session.add(log)
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                if user.role == 'main_admin':
                    next_page = url_for('admin.dashboard')
                elif user.role == 'admin':
                    next_page = url_for('faculty.dashboard')
                else:
                    next_page = url_for('student.dashboard')
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    from models.announcement_model import Announcement
    announcements = Announcement.query.order_by(Announcement.date.desc()).limit(3).all()
    return render_template('auth/login.html', announcements=announcements)

@auth_bp.route('/register')
def register():
    if current_user.is_authenticated:
        if current_user.role == 'main_admin':
            return redirect(url_for('admin.dashboard'))
        if current_user.role == 'admin':
            return redirect(url_for('faculty.dashboard'))
        return redirect(url_for('student.dashboard'))
    return render_template('auth/register.html')

@auth_bp.route('/register_faculty')
def register_faculty():
    if current_user.is_authenticated:
        if current_user.role == 'main_admin':
            return redirect(url_for('admin.dashboard'))
        if current_user.role == 'admin':
            return redirect(url_for('faculty.dashboard'))
        return redirect(url_for('student.dashboard'))
    return render_template('auth/faculty_registration.html')

@auth_bp.route('/register_main_admin')
def register_main_admin():
    if current_user.is_authenticated:
        if current_user.role == 'main_admin':
            return redirect(url_for('admin.dashboard'))
        if current_user.role == 'admin':
            return redirect(url_for('faculty.dashboard'))
        return redirect(url_for('student.dashboard'))
    return render_template('auth/main_admin_registration.html')

@auth_bp.route('/register_action', methods=['POST'])
def register_action():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role') # 'student' or 'admin'
    
    reg_no = request.form.get('reg_no')
    
    # Validation - Check for empty required fields
    if not name or not email or not password:
        flash('Please fill in all required fields (Name, Email, and Password).', 'danger')
        if role == 'admin':
            return redirect(url_for('auth.register_faculty'))
        return redirect(url_for('auth.register'))
    
    # Validation - Check for registration number for students
    if role == 'student' and not reg_no:
        flash('Registration number is required for student accounts.', 'danger')
        return redirect(url_for('auth.register'))
    
    # Validation - Check for duplicate email
    user = User.query.filter_by(email=email).first()
    if user:
        if user.status == 'blacklisted':
            flash('This account is blacklisted and cannot be recreated. Please contact administration.', 'danger')
        else:
            flash('This email is already registered! Please use a different email address or login if you already have an account.', 'warning')
        if role == 'admin':
            return redirect(url_for('auth.register_faculty'))
        return redirect(url_for('auth.register'))

    # Validation - Check for duplicate registration number (students only)
    if role == 'student' and reg_no:
        existing_reg = User.query.filter_by(reg_no=reg_no).first()
        if existing_reg:
            if existing_reg.status == 'blacklisted':
                flash('This registration number is blacklisted. Please contact administration.', 'danger')
            else:
                flash('This registration number already exists! Please check your registration number and enter the correct one.', 'warning')
            return redirect(url_for('auth.register'))

    new_user = User(name=name, email=email, role=role, reg_no=reg_no)
    
    if role == 'main_admin':
        new_user.designation = request.form.get('designation', 'Administrator')
        
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

    if role == 'main_admin':
        from models.settings_model import SystemSetting
        
        access_code = request.form.get('access_code')
        required_code = SystemSetting.get_setting('main_admin_access_code', default='SUPER_SECRET_NEXUS_2024')
        
        if access_code != required_code:
            flash('Invalid Master Registration Key. Registration denied.', 'danger')
            return redirect(url_for('auth.register_main_admin'))

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
            try:
                otp = user.generate_otp()
                db.session.commit()
                
                # Try sending email, catch errors to avoid 500
                success = send_otp_email(user, otp)
                
                from flask import session
                session['reset_email'] = email
                
                if success:
                    flash('Success! A 6-digit verification code is on its way.', 'info')
                else:
                    flash('Account found! (Developer Mode) Your OTP is displayed in a message above.', 'warning')
                
                return redirect(url_for('auth.verify_otp'))
            except Exception as e:
                db.session.rollback()
                print(f"ERROR in forgot_password: {str(e)}")
                import traceback
                traceback.print_exc()
                flash('An internal error occurred. Please try again later.', 'danger')
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
    
    # Check if mail is configured
    mail_user = current_app.config.get('MAIL_USERNAME')
    if not mail_user or 'your-email' in mail_user or not current_app.config.get('MAIL_PASSWORD'):
        print("\n" + "="*50)
        print(f"DEVELOPER MODE: OTP for {user.email} is: {otp}")
        print("="*50 + "\n")
        flash(f"DEVELOPER MODE OTP: {otp}", "warning")
        return False # Handled as dev fallback

    msg = Message('Your Password Reset OTP - CSE Nexus',
                  sender=mail_user,
                  recipients=[user.email])
    msg.body = f'''Your password reset OTP is: {otp}

This code will expire in 10 minutes. 

If you did not make this request then simply ignore this email and no changes will be made.
'''
    
    print(f"Attempting to send OTP email to {user.email} via {mail_user}")
    try:
        mail.send(msg)
        print("OTP email sent successfully!")
        return True
    except Exception as e:
        print(f"CRITICAL: Error sending email: {e}")
        print(f"FALLBACK: OTP for {user.email} is: {otp}")
        flash(f"Couldn't send email, using Dev Fallback OTP: {otp}", "warning")
        import traceback
        traceback.print_exc()
        return False

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
