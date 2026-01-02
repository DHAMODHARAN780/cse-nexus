import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models.announcement_model import Announcement
from models.user_model import User
from models.subject_model import Subject
from models.content_model import Content
from models.achievement_model import Achievement
from models.timetable_model import Timetable
from models.login_log_model import LoginLog
from models.settings_model import SystemSetting
from datetime import datetime
from flask import jsonify

faculty_bp = Blueprint('faculty', __name__, url_prefix='/admin')

def admin_required(f):
    # Decorator to ensure user is admin
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@faculty_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Overview stats
    student_count = User.query.filter_by(role='student', status='active').count()
    content_count = Content.query.count()
    subject_count = Subject.query.count()
    announcement_count = Announcement.query.count()
    achievement_count = Achievement.query.count()
    
    recent_uploads = Content.query.order_by(Content.upload_date.desc()).limit(5).all()
    recent_logins = LoginLog.query.order_by(LoginLog.login_time.desc()).limit(10).all()
    
    return render_template('faculty/dashboard.html', 
                           student_count=student_count, 
                           content_count=content_count,
                           subject_count=subject_count,
                           announcement_count=announcement_count,
                           achievement_count=achievement_count,
                           recent_uploads=recent_uploads,
                           recent_logins=recent_logins)

@faculty_bp.route('/content/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_content(id):
    content = Content.query.get_or_404(id)
    if request.method == 'POST':
        content.title = request.form.get('title')
        content.subject = request.form.get('subject')
        content.unit = request.form.get('unit')
        content.year = request.form.get('year')
        content.semester = request.form.get('semester')
        content.type = request.form.get('type')
        db.session.commit()
        flash('Content updated.', 'success')
        return redirect(url_for('faculty.manage_documents'))
    return render_template('faculty/edit_content.html', content=content)

@faculty_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload():
    if request.method == 'POST':
        title = request.form.get('title')
        ctype = request.form.get('type') # material, video
        subject = request.form.get('subject')
        unit = request.form.get('unit')
        year = request.form.get('year')
        semester = request.form.get('semester')
        
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            # Differentiate folders
            if ctype == 'video':
                subdir = 'videos'
            else:
                subdir = 'materials'
                
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subdir, filename)
            file.save(save_path)
            
            # DB entry - store path relative to static/
            rel_path = f'uploads/{subdir}/{filename}' 
            new_content = Content(
                title=title,
                type=ctype,
                filepath=rel_path,
                subject=subject,
                unit=unit,
                year=year,
                semester=semester,
                uploaded_by=current_user.id
            )
            db.session.add(new_content)
            
            # Post duplicate as announcement
            announce_title = f"New {ctype} for {subject}"
            announce_text = f"The {ctype} '{title}' for {subject} unit {unit} is now available in your course materials. Click to view or download."
            new_announce = Announcement(title=announce_title, text=announce_text, type='upload', posted_by=current_user.id, file_path=rel_path)
            db.session.add(new_announce)
            
            db.session.commit()
            flash('Content uploaded successfully!', 'success')
            return redirect(url_for('faculty.dashboard'))
            
    return render_template('faculty/upload.html')

@faculty_bp.route('/announcements/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_announcement(id):
    announce = Announcement.query.get_or_404(id)
    if request.method == 'POST':
        announce.title = request.form.get('title')
        announce.text = request.form.get('text')
        announce.type = request.form.get('type')
        db.session.commit()
        flash('Announcement updated.', 'success')
        return redirect(url_for('faculty.announcements'))
    return render_template('faculty/edit_announcement.html', announce=announce)

@faculty_bp.route('/announcements', methods=['GET', 'POST'])
@login_required
@admin_required
def announcements():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        atype = request.form.get('type')
        
        file = request.files.get('file')
        rel_path = None
        if file:
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images', filename)
            file.save(save_path)
            rel_path = f'uploads/images/{filename}'
            
        announce = Announcement(title=title, text=text, type=atype, posted_by=current_user.id, file_path=rel_path)
        db.session.add(announce)
        db.session.commit()
        flash('Announcement Posted', 'success')
        
    announcements = Announcement.query.order_by(Announcement.date.desc()).all()
    return render_template('faculty/announcements.html', announcements=announcements)

@faculty_bp.route('/api/subjects/<int:semester>')
@login_required
@admin_required
def get_subjects(semester):
    subjects = Subject.query.filter_by(semester=semester).all()
    return jsonify([{'id': s.id, 'title': s.title, 'code': s.code} for s in subjects])

# Achievement Management
@faculty_bp.route('/achievements', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_achievements():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image_url = request.form.get('image_url') # Link option
        
        # File option
        file = request.files.get('file')
        file_rel_path = None
        if file:
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images', filename)
            file.save(save_path)
            file_rel_path = f'uploads/images/{filename}'
        
        achievement = Achievement(
            title=title, 
            description=description, 
            image_url=image_url if not file_rel_path else file_rel_path, # Prioritize upload
            file_path=file_rel_path,
            posted_by=current_user.id
        )
        db.session.add(achievement)
        db.session.commit()
        flash('Achievement added successfully!', 'success')
        
    achievements = Achievement.query.order_by(Achievement.date.desc()).all()
    return render_template('faculty/manage_achievements.html', achievements=achievements)

@faculty_bp.route('/achievements/delete/<int:id>')
@login_required
@admin_required
def delete_achievement(id):
    achievement = Achievement.query.get_or_404(id)
    db.session.delete(achievement)
    db.session.commit()
    flash('Achievement deleted.', 'info')
    return redirect(url_for('faculty.manage_achievements'))

@faculty_bp.route('/achievements/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_achievement(id):
    achievement = Achievement.query.get_or_404(id)
    if request.method == 'POST':
        achievement.title = request.form.get('title')
        achievement.description = request.form.get('description')
        achievement.image_url = request.form.get('image_url')
        
        file = request.files.get('file')
        if file:
            # Cleanup old file if it exists in local storage
            if achievement.file_path:
                try:
                    # Construct full path for deletion
                    full_old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], achievement.file_path.replace('uploads/', ''))
                    if os.path.exists(full_old_path):
                        os.remove(full_old_path)
                except Exception as e:
                    print(f"Error removing old achievement file: {e}")
            
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images', filename)
            file.save(save_path)
            achievement.file_path = f'uploads/images/{filename}'
            achievement.image_url = achievement.file_path # Update image preview link
            
        db.session.commit()
        flash('Achievement updated successfully!', 'success')
        return redirect(url_for('faculty.manage_achievements'))
        
    return render_template('faculty/edit_achievement.html', achievement=achievement)

# Timetable Management
@faculty_bp.route('/timetable', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_timetable():
    if request.method == 'POST':
        title = request.form.get('title')
        semester = request.form.get('semester')
        year = request.form.get('year')
        file = request.files.get('file')
        
        if file:
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'timetables', filename)
            file.save(save_path)
            rel_path = f'uploads/timetables/{filename}'
            
            timetable = Timetable(
                title=title,
                semester=int(semester),
                year=int(year),
                file_path=rel_path,
                posted_by=current_user.id
            )
            db.session.add(timetable)
            db.session.commit()
            flash('Timetable uploaded successfully!', 'success')
        else:
            flash('Please select a file to upload.', 'warning')
            
    timetables = Timetable.query.order_by(Timetable.date_posted.desc()).all()
    return render_template('faculty/manage_timetable.html', timetables=timetables)

@faculty_bp.route('/timetable/delete/<int:id>')
@login_required
@admin_required
def delete_timetable(id):
    timetable = Timetable.query.get_or_404(id)
    db.session.delete(timetable)
    db.session.commit()
    flash('Timetable deleted.', 'info')
    return redirect(url_for('faculty.manage_timetable'))

@faculty_bp.route('/timetable/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_timetable(id):
    timetable = Timetable.query.get_or_404(id)
    if request.method == 'POST':
        timetable.title = request.form.get('title')
        timetable.semester = int(request.form.get('semester'))
        timetable.year = int(request.form.get('year'))
        
        file = request.files.get('file')
        if file:
            # Delete old file
            try:
                if os.path.exists(timetable.file_path):
                    os.remove(timetable.file_path)
            except Exception as e:
                print(f"Error removing old timetable file: {e}")
                
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'timetables', filename)
            file.save(save_path)
            timetable.file_path = f'static/uploads/timetables/{filename}'
            
        db.session.commit()
        flash('Timetable updated successfully!', 'success')
        return redirect(url_for('faculty.manage_timetable'))
        
    return render_template('faculty/edit_timetable.html', timetable=timetable)

@faculty_bp.route('/content/delete/<int:id>')
@login_required
@admin_required
def delete_content(id):
    content = Content.query.get_or_404(id)
    # Remove file from disk
    try:
        if os.path.exists(content.filepath):
            os.remove(content.filepath)
    except Exception as e:
        print(f"Error removing file: {e}")
        
    db.session.delete(content)
    db.session.commit()
    flash('Content deleted successfully.', 'info')
    return redirect(url_for('faculty.manage_documents'))

@faculty_bp.route('/announcement/delete/<int:id>')
@login_required
@admin_required
def delete_announcement(id):
    announce = Announcement.query.get_or_404(id)
    # Clean up attachment if any
    if announce.file_path:
        try:
            if os.path.exists(announce.file_path):
                os.remove(announce.file_path)
        except Exception as e:
            print(f"Error removing file: {e}")
            
    db.session.delete(announce)
    db.session.commit()
    flash('Announcement deleted.', 'info')
    return redirect(url_for('faculty.announcements'))

@faculty_bp.route('/documents')
@login_required
@admin_required
def manage_documents():
    # Aggregate all types of documents
    raw_materials = Content.query.order_by(Content.semester, Content.subject, Content.unit).all()
    
    # Group materials by semester, subject and unit
    materials = {}
    for m in raw_materials:
        if m.semester not in materials:
            materials[m.semester] = {}
        if m.subject not in materials[m.semester]:
            materials[m.semester][m.subject] = {}
        if m.unit not in materials[m.semester][m.subject]:
            materials[m.semester][m.subject][m.unit] = []
        materials[m.semester][m.subject][m.unit].append(m)
        
    announc_docs = Announcement.query.filter(Announcement.file_path != None).order_by(Announcement.date.desc()).all()
    achieve_docs = Achievement.query.filter(Achievement.file_path != None).order_by(Achievement.date.desc()).all()
    
    raw_timetables = Timetable.query.order_by(Timetable.year.desc(), Timetable.semester.asc()).all()
    timetables = {}
    for t in raw_timetables:
        if t.year not in timetables:
            timetables[t.year] = []
        timetables[t.year].append(t)
    
    return render_template('faculty/manage_documents.html',
                           materials=materials,
                           announc_docs=announc_docs,
                           achieve_docs=achieve_docs,
                           timetables=timetables)

@faculty_bp.route('/students')
@login_required
@admin_required
def manage_students():
    # Group students by year and sort alphabetically
    all_students = User.query.filter_by(role='student').order_by(User.year.desc(), User.name.asc()).all()
    
    students_by_year = {}
    for s in all_students:
        if s.year not in students_by_year:
            students_by_year[s.year] = []
        students_by_year[s.year].append(s)
        
    return render_template('faculty/manage_students.html', students_by_year=students_by_year)
@faculty_bp.route('/students/blacklist/<int:id>')
@login_required
@admin_required
def blacklist_student(id):
    student = User.query.get_or_404(id)
    if student.role == 'admin':
        flash('Cannot blacklist an admin account.', 'danger')
    else:
        student.status = 'blacklisted'
        db.session.commit()
        flash(f'Student {student.name} has been blacklisted.', 'success')
    return redirect(url_for('faculty.manage_students'))

@faculty_bp.route('/students/remove/<int:id>')
@login_required
@admin_required
def remove_student(id):
    student = User.query.get_or_404(id)
    if student.role == 'admin':
        flash('Cannot remove an admin account.', 'danger')
    else:
        name = student.name
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {name} has been permanently removed.', 'success')
    return redirect(url_for('faculty.manage_students'))

@faculty_bp.route('/settings')
@login_required
@admin_required
def settings():
    current_code = SystemSetting.get_setting('faculty_access_code', default=current_app.config.get('FACULTY_ACCESS_CODE'))
    return render_template('faculty/settings.html', current_code=current_code, read_only=True)
