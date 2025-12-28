from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
import os

from extensions import db, login_manager, migrate
from models.user_model import User
from models.content_model import Content
from models.announcement_model import Announcement
from models.login_log_model import LoginLog
from models.subject_model import Subject
from models.achievement_model import Achievement
from models.timetable_model import Timetable

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    from extensions import mail
    mail.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Ensure upload directories exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'materials'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'timetables'), exist_ok=True)

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.faculty_routes import faculty_bp
    from routes.student_routes import student_bp
    from routes.common_routes import common_bp
    # from routes.admin_routes import admin_bp # Merged into faculty/auth as per plan

    app.register_blueprint(auth_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(common_bp)
    
    # Context processor to inject global variables into templates
    @app.context_processor
    def inject_global_vars():
        from models.announcement_model import Announcement
        # Running updates for the marquee
        updates = Announcement.query.order_by(Announcement.date.desc()).limit(5).all()
        return dict(running_updates=updates)

    # Create tables within context
    with app.app_context():
        db.create_all()
        


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
