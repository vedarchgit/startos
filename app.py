"""app.py — App factory + /setup seed route"""
import os
from flask import Flask, redirect, url_for
from config     import config
from extensions import db, login_manager, csrf, limiter


def create_app(cfg=None):
    if cfg is None:
        cfg = os.getenv('FLASK_ENV', 'development')
    app = Flask(__name__)
    app.config.from_object(config.get(cfg, config['default']))

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    from models import User
    @login_manager.user_loader
    def load_user(uid):
        return db.session.get(User, int(uid))

    from routes.auth    import auth_bp
    from routes.student import student_bp
    from routes.admin   import admin_bp
    from routes.api     import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        from flask_login import current_user
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return redirect(url_for('admin.dashboard') if current_user.is_admin
                        else url_for('student.dashboard'))

    @app.route('/setup')
    def setup():
        """Visit once: http://127.0.0.1:5000/setup"""
        with app.app_context():
            db.create_all()
            _seed()
        return ('<h2 style="font-family:monospace;padding:40px;color:#0d0">'
                '&#10003; Database ready. <a href="/">Go to app</a></h2>')

    @app.errorhandler(404)
    def e404(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def e500(e):
        from flask import render_template
        app.logger.error(f'500: {e}')
        return render_template('errors/500.html'), 500

    @app.errorhandler(429)
    def e429(e):
        from flask import render_template
        return render_template('errors/429.html'), 429

    return app


def _seed():
    from models import (User, Skill, RiskParam, LabTask,
                        Organization, Project, ProjectRequirement)
    from werkzeug.security import generate_password_hash
    if User.query.first():
        return

    users = [
        User(username='admin',   email='admin@stratos.edu',
             password=generate_password_hash('admin123'),    role='Admin'),
        User(username='alice',   email='alice@student.edu',
             password=generate_password_hash('password123'), role='Student',
             branch='Computer', year=2),
        User(username='bob',     email='bob@student.edu',
             password=generate_password_hash('password123'), role='Student',
             branch='IT',       year=2),
        User(username='charlie', email='charlie@student.edu',
             password=generate_password_hash('password123'), role='Student',
             branch='Computer', year=3),
    ]
    db.session.add_all(users)
    db.session.flush()

    skill_data = [
        ('Python',           'Programming', 'General-purpose scripting',      4, 6, 8),
        ('SQL',              'Database',    'Structured Query Language',       6, 7, 6),
        ('UI Design',        'Design',      'User interface & UX',             5, 5, 7),
        ('Data Entry',       'Operations',  'Manual data input',               9, 9, 2),
        ('Machine Learning', 'AI/ML',       'Statistical learning',            3, 4, 9),
        ('Excel/Sheets',     'Operations',  'Spreadsheet automation',          8, 8, 3),
        ('Cloud (AWS)',      'DevOps',      'AWS infrastructure',              5, 5, 8),
    ]
    skills = []
    for name, cat, desc, rep, threat, comp in skill_data:
        s = Skill(name=name, category=cat, description=desc)
        db.session.add(s)
        db.session.flush()
        db.session.add(RiskParam(skill_id=s.skill_id,
                                  repetitiveness=rep,
                                  ai_threat_level=threat,
                                  complexity=comp))
        skills.append(s)

    task_data = [
        (0,'Hello World & Variables',  'Basic Python syntax',           'Easy',   0.5),
        (0,'Functions and Loops',      'Reusable functions + iteration','Medium', 1.0),
        (0,'Build a Flask REST API',   'API with 3 endpoints',          'Hard',   2.0),
        (1,'Basic SELECT Queries',     'WHERE and ORDER BY',            'Easy',   0.5),
        (1,'JOIN Queries',             'Combine multiple tables',       'Medium', 1.0),
        (1,'Normalized Schema Design', '3NF schema',                    'Hard',   2.0),
        (2,'Wireframe a Login Page',   'Annotated UI wireframe',        'Easy',   0.5),
        (2,'Design a Dashboard',       'Full responsive dashboard',     'Hard',   2.0),
        (3,'Data Cleaning Exercise',   'Clean 500-row CSV',             'Easy',   0.5),
        (4,'Linear Regression',        'Build and evaluate LR model',   'Medium', 1.0),
        (4,'Neural Network Keras',     'Train NN on MNIST',             'Hard',   2.0),
    ]
    for idx, title, desc, diff, weight in task_data:
        db.session.add(LabTask(skill_id=skills[idx].skill_id, title=title,
                               description=desc, difficulty=diff,
                               difficulty_weight=weight))

    orgs = [
        Organization(name='TechCorp India',     industry='Technology'),
        Organization(name='DataSoft Solutions', industry='Analytics'),
        Organization(name='SkillBridge NGO',    industry='Education'),
    ]
    db.session.add_all(orgs)
    db.session.flush()

    from datetime import date
    projs = [
        Project(org_id=orgs[0].org_id, title='Web Analytics Dashboard',
                description='Flask + SQL real-time dashboard', deadline=date(2025,6,30)),
        Project(org_id=orgs[0].org_id, title='AI Chatbot Backend',
                description='Python ML customer support bot',  deadline=date(2025,7,15)),
        Project(org_id=orgs[1].org_id, title='SQL Reporting Suite',
                description='Automated PDF reports from MySQL',deadline=date(2025,5,31)),
        Project(org_id=orgs[2].org_id, title='Student Skill Tracker',
                description='Simple school progress tracker',  deadline=date(2025,8,1)),
    ]
    db.session.add_all(projs)
    db.session.flush()

    for pi, si, md in [(0,0,60),(0,1,50),(1,0,70),(1,4,55),
                       (2,1,75),(3,0,50),(3,2,40)]:
        db.session.add(ProjectRequirement(
            project_id=projs[pi].project_id,
            skill_id=skills[si].skill_id,
            min_depth=md))
    db.session.commit()
    print("✓ Seed complete")


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
