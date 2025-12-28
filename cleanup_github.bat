@echo off
echo Cleaning up duplicate files from GitHub repository...
echo.

REM Remove duplicate HTML files (they're in templates/)
git rm __init__.py
git rm achievement_model.py
git rm achievements.html
git rm admin_routes.py
git rm announcement_model.py
git rm announcements.html
git rm auth_routes.py
git rm auth_service.py
git rm base.html
git rm common_routes.py
git rm constants.py
git rm content_model.py
git rm curriculum.html
git rm dashboard.html
git rm decorators.py
git rm doubts.html
git rm edit_achievement.html
git rm edit_announcement.html
git rm edit_content.html
git rm edit_timetable.html
git rm events.html
git rm faculty_registration.html
git rm faculty_routes.py
git rm forgot_password.html
git rm helpers.py
git rm launch.json
git rm login.html
git rm login_log_model.py
git rm manage_achievements.html
git rm manage_announcements.html
git rm manage_documents.html
git rm manage_slider.html
git rm manage_students.html
git rm manage_timetable.html
git rm notification_service.py
git rm profile.html
git rm rag_service.py
git rm register.html
git rm reset_password.html
git rm settings.html
git rm settings_model.py
git rm student_dashboard.html
git rm student_routes.py
git rm subject.html
git rm subject_model.py
git rm timetable.html
git rm timetable_model.py
git rm unit_content.html
git rm units.html
git rm upload.html
git rm upload_materials.html
git rm upload_service.py
git rm upload_video.html
git rm user_model.py
git rm verify_otp.html
git rm view_content.html
git rm view_login_logs.html
git rm year_sem.html

REM Remove .pyc files (compiled Python - shouldn't be on GitHub)
git rm app.cpython-311.pyc
git rm config.cpython-311.pyc
git rm config.cpython-314.pyc
git rm extensions.cpython-311.pyc
git rm extensions.cpython-314.pyc
git rm nexus.cpython-311.pyc
git rm nexus.cpython-314.pyc

echo.
echo Committing changes...
git commit -m "Clean up: Removed duplicate files from root directory"

echo.
echo Pushing to GitHub...
git push

echo.
echo Done! Your GitHub repository is now clean and organized.
pause
