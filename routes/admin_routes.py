import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models.user_model import User
from models.login_log_model import LoginLog
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/main-admin')

def main_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'main_admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@main_admin_required
def dashboard():
    faculty_count = User.query.filter_by(role='admin').count()
    student_count = User.query.filter_by(role='student').count()
    recent_logins = LoginLog.query.order_by(LoginLog.login_time.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                           faculty_count=faculty_count, 
                           student_count=student_count,
                           recent_logins=recent_logins)

@admin_bp.route('/faculties')
@login_required
@main_admin_required
def monitor_faculties():
    faculties = User.query.filter_by(role='admin').order_by(User.name).all()
    return render_template('admin/monitor_faculties.html', faculties=faculties)

@admin_bp.route('/students')
@login_required
@main_admin_required
def monitor_students():
    students = User.query.filter_by(role='student').order_by(User.name).all()
    return render_template('admin/monitor_students.html', students=students)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@main_admin_required
def settings():
    from models.settings_model import SystemSetting
    if request.method == 'POST':
        access_code = request.form.get('access_code')
        main_admin_code = request.form.get('main_admin_code')
        
        if access_code:
            SystemSetting.set_setting('faculty_access_code', access_code, 'Secret code required for faculty registration')
            flash('Faculty Access Code updated!', 'success')
        
        if main_admin_code:
            SystemSetting.set_setting('main_admin_access_code', main_admin_code, 'Secret code required for Main Admin registration')
            flash('Main Admin Access Code updated!', 'success')
            
        return redirect(url_for('admin.settings'))
    
    faculty_code = SystemSetting.get_setting('faculty_access_code', default=current_app.config.get('FACULTY_ACCESS_CODE'))
    main_admin_code = SystemSetting.get_setting('main_admin_access_code', default='SUPER_SECRET_NEXUS_2024')
    
    return render_template('admin/settings.html', faculty_code=faculty_code, main_admin_code=main_admin_code)

@admin_bp.route('/user/<int:id>/toggle-status')
@login_required
@main_admin_required
def toggle_user_status(id):
    user = User.query.get_or_404(id)
    if user.status == 'active':
        user.status = 'blacklisted'
    else:
        user.status = 'active'
    db.session.commit()
    flash(f'Status for {user.name} updated to {user.status}.', 'success')
    return redirect(request.referrer or url_for('admin.dashboard'))
