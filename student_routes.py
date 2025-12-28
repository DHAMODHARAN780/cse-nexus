import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_required, current_user
from extensions import db
from models.content_model import Content
from models.announcement_model import Announcement
from models.user_model import User
from models.subject_model import Subject
from models.achievement_model import Achievement
from models.timetable_model import Timetable

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('faculty.dashboard'))
        
    # Show subjects relevant to student's semester from the curriculum
    subjects = Subject.query.filter_by(semester=current_user.semester).order_by(Subject.code).all()
    
    # Fetch recent data for dashboard
    announcements = Announcement.query.order_by(Announcement.date.desc()).limit(5).all()
    achievements = Achievement.query.order_by(Achievement.date.desc()).limit(3).all()
    
    # Fetch all relevant timetables for student's year/semester
    timetables = Timetable.query.filter_by(
        year=int(current_user.year), 
        semester=int(current_user.semester)
    ).order_by(Timetable.date_posted.desc()).all()
    
    return render_template('student/dashboard.html', 
                           subjects=subjects, 
                           announcements=announcements,
                           achievements=achievements,
                           timetables=timetables)

@student_bp.route('/content/<subject>')
@login_required
def view_subject(subject):
    # Get all units
    units = {}
    for i in range(1, 6):
        materials = Content.query.filter_by(
            subject=subject, 
            unit=i, 
            type='material'
        ).all()
        videos = Content.query.filter_by(
            subject=subject, 
            unit=i, 
            type='video'
        ).all()
        if materials or videos:
            units[i] = {'materials': materials, 'videos': videos}
            
    return render_template('student/view_content.html', subject=subject, units=units)

@student_bp.route('/doubts', methods=['GET', 'POST'])
@login_required
def doubts():
    from flask import session
    from services.rag_service import rag_service
    
    # Initialize chat history if not exists
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    ai_response = None
    query = ''
    sources = []
    
    if request.method == 'POST':
        query = request.form.get('doubt')
        
        if query:
            # First, try to find relevant PDFs based on keyword matching
            relevant_content = Content.query.filter(
                (Content.title.ilike(f'%{query}%')) | 
                (Content.subject.ilike(f'%{query}%'))
            ).limit(3).all()
            
            # If no keyword matches, get some general course materials from student's semester
            if not relevant_content:
                relevant_content = Content.query.filter_by(
                    semester=current_user.semester
                ).limit(3).all()
            
            # Use AI to answer the question with history
            result = rag_service.answer_doubt(query, relevant_content, session['chat_history'])
            ai_response = result['answer']
            sources = result['sources']
            
            # Append to history
            session['chat_history'].append({'role': 'user', 'content': query})
            session['chat_history'].append({
                'role': 'assistant', 
                'content': ai_response,
                'sources': sources
            })
            session.modified = True
            
    return render_template('student/doubts.html', 
                         chat_history=session['chat_history'],
                         query=query)

@student_bp.route('/doubts/clear')
@login_required
def clear_doubts():
    from flask import session
    session.pop('chat_history', None)
    return redirect(url_for('student.doubts'))

@student_bp.route('/curriculum')
@login_required
def curriculum():
    # Group subjects by semester
    all_subjects = Subject.query.order_by(Subject.semester, Subject.code).all()
    curriculum_data = {}
    for sub in all_subjects:
        if sub.semester not in curriculum_data:
            curriculum_data[sub.semester] = []
        curriculum_data[sub.semester].append(sub)
    
    return render_template('student/curriculum.html', curriculum=curriculum_data)
