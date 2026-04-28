from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

# ── Association tables ────────────────────────────────────────
skill_dependency = db.Table('skill_dependency',
    db.Column('skill_id',     db.Integer, db.ForeignKey('skills.skill_id',    ondelete='CASCADE'), primary_key=True),
    db.Column('prerequisite', db.Integer, db.ForeignKey('skills.skill_id',    ondelete='CASCADE'), primary_key=True),
)
student_project = db.Table('student_project',
    db.Column('student_id',  db.Integer, db.ForeignKey('users.user_id',       ondelete='CASCADE'), primary_key=True),
    db.Column('project_id',  db.Integer, db.ForeignKey('projects.project_id', ondelete='CASCADE'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow),
)

# ── User ──────────────────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username   = db.Column(db.String(50),  nullable=False, unique=True)
    email      = db.Column(db.String(100), nullable=False, unique=True)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.Enum('Student','Admin'), nullable=False, default='Student')
    branch     = db.Column(db.String(50),  nullable=True)
    year       = db.Column(db.SmallInteger, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self): return str(self.user_id)

    @property
    def is_admin(self): return self.role == 'Admin'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    skills   = db.relationship('StudentSkill', back_populates='student', cascade='all, delete-orphan')
    attempts = db.relationship('TaskAttempt',  back_populates='student', cascade='all, delete-orphan')
    projects = db.relationship('Project', secondary=student_project, back_populates='students')

# ── Skill ─────────────────────────────────────────────────────
class Skill(db.Model):
    __tablename__ = 'skills'
    skill_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.String(100), nullable=False, unique=True)
    category    = db.Column(db.String(50),  nullable=False)
    description = db.Column(db.Text, nullable=True)

    risk_param   = db.relationship('RiskParam',   back_populates='skill', uselist=False, cascade='all, delete-orphan')
    lab_tasks    = db.relationship('LabTask',      back_populates='skill', cascade='all, delete-orphan')
    student_data = db.relationship('StudentSkill', back_populates='skill', cascade='all, delete-orphan')

# ── RiskParam ─────────────────────────────────────────────────
class RiskParam(db.Model):
    __tablename__ = 'risk_params'
    param_id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_id        = db.Column(db.Integer, db.ForeignKey('skills.skill_id', ondelete='CASCADE'), nullable=False, unique=True)
    repetitiveness  = db.Column(db.SmallInteger, nullable=False)
    ai_threat_level = db.Column(db.SmallInteger, nullable=False)
    complexity      = db.Column(db.SmallInteger, nullable=False)

    skill = db.relationship('Skill', back_populates='risk_param')

    @property
    def base_risk_score(self):
        raw = (self.repetitiveness + self.ai_threat_level - self.complexity / 2.0) * 10
        return round(max(0, min(100, raw)), 1)

# ── StudentSkill ──────────────────────────────────────────────
class StudentSkill(db.Model):
    __tablename__ = 'student_skills'
    student_id  = db.Column(db.Integer, db.ForeignKey('users.user_id',   ondelete='CASCADE'), primary_key=True)
    skill_id    = db.Column(db.Integer, db.ForeignKey('skills.skill_id', ondelete='CASCADE'), primary_key=True)
    depth_score = db.Column(db.Numeric(5, 2), default=0.00)
    risk_score  = db.Column(db.Numeric(5, 2), nullable=True)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('User',  back_populates='skills')
    skill   = db.relationship('Skill', back_populates='student_data')

    @property
    def risk_level(self):
        if self.risk_score is None: return 'UNKNOWN'
        s = float(self.risk_score)
        if s >= 70: return 'HIGH'
        if s >= 40: return 'MEDIUM'
        return 'LOW'

    def recalculate_risk(self):
        rp = self.skill.risk_param
        if not rp: return
        raw = (rp.repetitiveness + rp.ai_threat_level - rp.complexity / 2.0) \
              * (1.0 - float(self.depth_score) / 100.0) * 10
        self.risk_score = round(max(0, min(100, raw)), 2)

# ── LabTask ───────────────────────────────────────────────────
class LabTask(db.Model):
    __tablename__ = 'lab_tasks'
    task_id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_id          = db.Column(db.Integer, db.ForeignKey('skills.skill_id', ondelete='CASCADE'), nullable=False)
    title             = db.Column(db.String(200), nullable=False)
    description       = db.Column(db.Text, nullable=True)
    difficulty        = db.Column(db.Enum('Easy','Medium','Hard'), nullable=False)
    difficulty_weight = db.Column(db.Numeric(3, 2), nullable=False)
    max_score         = db.Column(db.Integer, nullable=False, default=100)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)

    skill    = db.relationship('Skill',       back_populates='lab_tasks')
    attempts = db.relationship('TaskAttempt', back_populates='task', cascade='all, delete-orphan')

# ── TaskAttempt ───────────────────────────────────────────────
class TaskAttempt(db.Model):
    __tablename__ = 'task_attempts'
    attempt_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id     = db.Column(db.Integer, db.ForeignKey('users.user_id',     ondelete='CASCADE'), nullable=False)
    task_id        = db.Column(db.Integer, db.ForeignKey('lab_tasks.task_id', ondelete='CASCADE'), nullable=False)
    score_achieved = db.Column(db.Numeric(5, 2), nullable=False)
    attempted_at   = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User',    back_populates='attempts')
    task    = db.relationship('LabTask', back_populates='attempts')

# ── Organization ──────────────────────────────────────────────
class Organization(db.Model):
    __tablename__ = 'organizations'
    org_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name     = db.Column(db.String(150), nullable=False, unique=True)
    industry = db.Column(db.String(100), nullable=True)
    website  = db.Column(db.String(200), nullable=True)
    projects = db.relationship('Project', back_populates='org', cascade='all, delete-orphan')

# ── Project ──────────────────────────────────────��────────────
class Project(db.Model):
    __tablename__ = 'projects'
    project_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_id      = db.Column(db.Integer, db.ForeignKey('organizations.org_id', ondelete='CASCADE'), nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline    = db.Column(db.Date, nullable=True)
    posted_at   = db.Column(db.DateTime, default=datetime.utcnow)

    org          = db.relationship('Organization', back_populates='projects')
    requirements = db.relationship('ProjectRequirement', back_populates='project', cascade='all, delete-orphan')
    students     = db.relationship('User', secondary=student_project, back_populates='projects')

# ── ProjectRequirement ────────────────────────────────────────
class ProjectRequirement(db.Model):
    __tablename__ = 'project_requirements'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id', ondelete='CASCADE'), primary_key=True)
    skill_id   = db.Column(db.Integer, db.ForeignKey('skills.skill_id',     ondelete='CASCADE'), primary_key=True)
    min_depth  = db.Column(db.Numeric(5, 2), nullable=False, default=50.00)

    project = db.relationship('Project', back_populates='requirements')
    skill   = db.relationship('Skill')
