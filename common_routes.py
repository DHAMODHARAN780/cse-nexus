import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db

from models.achievement_model import Achievement
from models.timetable_model import Timetable
from sqlalchemy import text

common_bp = Blueprint('common', __name__)

@common_bp.route('/fix-db-schema')
def fix_db_schema():
    try:
        # Check dialect
        engine = db.engine
        dialect = engine.dialect.name
        
        if dialect == 'postgresql':
            with engine.connect() as conn:
                conn.execute(text('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(256);'))
                conn.commit()
            return "Success: PostgreSQL password_hash column resized to 256."
        elif dialect == 'sqlite':
            return "SQLite detected. No ALTER needed usually, or not supported easily."
        else:
            return f"Unknown dialect: {dialect}"
            
    except Exception as e:
        return f"Error: {str(e)}"

@common_bp.route('/achievements')
@login_required
def achievements():
    achievements = Achievement.query.order_by(Achievement.date.desc()).all()
    return render_template('common/achievements.html', achievements=achievements)

@common_bp.route('/timetable')
@login_required
def timetable():
    timetables = Timetable.query.order_by(Timetable.semester, Timetable.date_posted.desc()).all()
    return render_template('common/timetable.html', timetables=timetables)

@common_bp.route('/events')
@login_required
def events():
    return render_template('common/events.html')

@common_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST' and current_user.role == 'student':
        current_user.reg_no = request.form.get('reg_no')
        current_user.year = int(request.form.get('year'))
        current_user.semester = int(request.form.get('semester'))
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile: Registration number might already be in use.', 'danger')
            
        return redirect(url_for('common.profile'))
        
    return render_template('common/profile.html')
