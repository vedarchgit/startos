#!/bin/bash

# STRATOS-DB Setup Script for Ubuntu/Linux
# Run this to set up the entire project

set -e

echo "======================================"
echo "  STRATOS-DB Setup for Ubuntu"
echo "======================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Install it with: sudo apt-get install python3 python3-pip python3-venv"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --quiet --upgrade pip
echo "✓ Pip upgraded"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --quiet -r requirements.txt
echo "✓ Dependencies installed"

# Initialize database
echo ""
echo "Initializing SQLite database..."
python3 << 'EOF'
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
EOF

echo "✓ Database initialized with demo data"
echo ""
echo "======================================"
echo "  Setup Complete!"
echo "======================================"
echo ""
echo "To start the app, run:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source .venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open: http://localhost:5000"
echo ""
echo "Demo Credentials:"
echo "  Admin:    admin / admin123"
echo "  Students: student1-3 / student123"
echo ""
