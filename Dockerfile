FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Initialize database on container startup
RUN python << 'EOF'
from app import app, db
from models import User, Skill, RiskParam

with app.app_context():
    db.create_all()
    
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@stratos.edu', role='Admin')
        admin.set_password('admin123')
        db.session.add(admin)
    
    for i in range(1, 4):
        if not User.query.filter_by(username=f'student{i}').first():
            s = User(username=f'student{i}', email=f'student{i}@stratos.edu', role='Student', branch='CSE', year=2)
            s.set_password('student123')
            db.session.add(s)
    
    for name, cat in [('Python', 'Programming'), ('JavaScript', 'Programming'), ('Database Design', 'Database'), ('Web Development', 'Web')]:
        if not Skill.query.filter_by(name=name).first():
            skill = Skill(name=name, category=cat, description=f'{name} fundamentals')
            db.session.add(skill)
            db.session.flush()
            risk = RiskParam(skill_id=skill.skill_id, repetitiveness=5, ai_threat_level=6, complexity=7)
            db.session.add(risk)
    
    db.session.commit()
EOF

CMD ["python", "app.py"]
