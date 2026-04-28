@echo off
REM STRATOS-DB Setup Script for Windows
REM Run this to set up the entire project

echo ======================================
echo   STRATOS-DB Setup for Windows
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Download Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
call .venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --quiet --upgrade pip
echo Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed
echo.

REM Initialize database
echo Initializing SQLite database...
python << 'PYTHON_EOF'
from app import app, db
from models import User, Skill, RiskParam

with app.app_context():
    db.create_all()
    
    # Create admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@stratos.edu', role='Admin')
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Create sample students
    students_data = [
        ('student1', 'student1@stratos.edu', 'CSE', 2),
        ('student2', 'student2@stratos.edu', 'CSE', 3),
        ('student3', 'student3@stratos.edu', 'ECE', 2),
    ]
    
    for username, email, branch, year in students_data:
        student = User.query.filter_by(username=username).first()
        if not student:
            student = User(username=username, email=email, role='Student', branch=branch, year=year)
            student.set_password('student123')
            db.session.add(student)
    
    # Create skills
    skills_data = [
        ('Python', 'Programming'),
        ('JavaScript', 'Programming'),
        ('Database Design', 'Database'),
        ('Web Development', 'Web'),
        ('Cloud Computing', 'DevOps'),
    ]
    
    for skill_name, category in skills_data:
        skill = Skill.query.filter_by(name=skill_name).first()
        if not skill:
            skill = Skill(name=skill_name, category=category, description=f'{skill_name} fundamentals and advanced concepts')
            db.session.add(skill)
            db.session.flush()
            risk = RiskParam(skill_id=skill.skill_id, repetitiveness=5, ai_threat_level=6, complexity=7)
            db.session.add(risk)
    
    db.session.commit()
PYTHON_EOF

echo Database initialized with demo data
echo.
echo ======================================
echo   Setup Complete!
echo ======================================
echo.
echo To start the app, run:
echo   run.bat
echo.
echo Or manually:
echo   .venv\Scripts\activate.bat
echo   python app.py
echo.
echo Then open: http://localhost:5000
echo.
echo Demo Credentials:
echo   Admin:    admin / admin123
echo   Students: student1-3 / student123
echo.
pause
