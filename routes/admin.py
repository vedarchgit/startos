from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import (User, Skill, RiskParam, StudentSkill, LabTask,
                    TaskAttempt, Organization, Project, ProjectRequirement)
from sqlalchemy import func
import csv, io

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def dec(*a, **kw):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*a, **kw)
    return dec

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    student_count = User.query.filter_by(role='Student').count()
    skill_count   = Skill.query.count()
    attempt_count = TaskAttempt.query.count()
    project_count = Project.query.count()

    top_students = (db.session.query(
            User.username, User.branch,
            func.round(func.avg(StudentSkill.depth_score),1).label('avg_depth'),
            func.round(func.avg(StudentSkill.risk_score), 1).label('avg_risk'),
            func.count(StudentSkill.skill_id).label('skill_count'))
        .join(StudentSkill, StudentSkill.student_id == User.user_id)
        .filter(User.role=='Student')
        .group_by(User.user_id, User.username, User.branch)
        .order_by(func.avg(StudentSkill.depth_score).desc()).limit(5).all())

    high_risk = (db.session.query(Skill, RiskParam)
        .join(RiskParam, RiskParam.skill_id == Skill.skill_id)
        .order_by((RiskParam.repetitiveness + RiskParam.ai_threat_level
                   - RiskParam.complexity / 2.0).desc()).limit(5).all())

    recent = (db.session.query(TaskAttempt, User, LabTask)
        .join(User,    TaskAttempt.student_id == User.user_id)
        .join(LabTask, TaskAttempt.task_id    == LabTask.task_id)
        .order_by(TaskAttempt.attempted_at.desc()).limit(8).all())

    return render_template('admin/dashboard.html',
        student_count=student_count, skill_count=skill_count,
        attempt_count=attempt_count, project_count=project_count,
        top_students=top_students, high_risk=high_risk, recent=recent)

@admin_bp.route('/skills', methods=['GET','POST'])
@login_required
@admin_required
def manage_skills():
    if request.method == 'POST':
        name  = request.form.get('name','').strip()
        cat   = request.form.get('category','').strip()
        desc  = request.form.get('description','').strip()
        rep   = int(request.form.get('repetitiveness',5))
        threat= int(request.form.get('ai_threat_level',5))
        comp  = int(request.form.get('complexity',5))
        if Skill.query.filter_by(name=name).first():
            flash(f'"{name}" already exists.', 'danger')
        else:
            s = Skill(name=name, category=cat, description=desc)
            db.session.add(s); db.session.flush()
            db.session.add(RiskParam(skill_id=s.skill_id,
                repetitiveness=rep, ai_threat_level=threat, complexity=comp))
            db.session.commit()
            flash(f'Skill "{name}" added!', 'success')
    skills = (db.session.query(Skill, RiskParam)
        .outerjoin(RiskParam, RiskParam.skill_id == Skill.skill_id)
        .order_by(Skill.category, Skill.name).all())
    return render_template('admin/skills.html', skills=skills)

@admin_bp.route('/tasks', methods=['GET','POST'])
@login_required
@admin_required
def manage_tasks():
    all_skills = Skill.query.order_by(Skill.name).all()
    if request.method == 'POST':
        wmap = {'Easy':0.5,'Medium':1.0,'Hard':2.0}
        diff = request.form.get('difficulty','Medium')
        db.session.add(LabTask(
            skill_id=int(request.form.get('skill_id')),
            title=request.form.get('title','').strip(),
            description=request.form.get('description','').strip(),
            difficulty=diff, difficulty_weight=wmap[diff]))
        db.session.commit()
        flash('Task added!', 'success')
    tasks = (db.session.query(LabTask, Skill,
             func.count(TaskAttempt.attempt_id).label('cnt'))
        .join(Skill, LabTask.skill_id == Skill.skill_id)
        .outerjoin(TaskAttempt, TaskAttempt.task_id == LabTask.task_id)
        .group_by(LabTask.task_id, Skill.skill_id)
        .order_by(Skill.name, LabTask.difficulty).all())
    return render_template('admin/tasks.html', tasks=tasks, skills=all_skills)

@admin_bp.route('/students')
@login_required
@admin_required
def manage_students():
    students = (db.session.query(User,
            func.round(func.avg(StudentSkill.depth_score),1).label('avg_depth'),
            func.round(func.avg(StudentSkill.risk_score), 1).label('avg_risk'),
            func.count(func.distinct(StudentSkill.skill_id)).label('skill_count'),
            func.count(func.distinct(TaskAttempt.attempt_id)).label('attempt_count'))
        .outerjoin(StudentSkill, StudentSkill.student_id == User.user_id)
        .outerjoin(TaskAttempt,  TaskAttempt.student_id  == User.user_id)
        .filter(User.role=='Student')
        .group_by(User.user_id)
        .order_by(func.avg(StudentSkill.depth_score).desc().nullslast()).all())
    return render_template('admin/students.html', students=students)

@admin_bp.route('/projects', methods=['GET','POST'])
@login_required
@admin_required
def manage_projects():
    all_skills = Skill.query.order_by(Skill.name).all()
    all_orgs   = Organization.query.order_by(Organization.name).all()
    if request.method == 'POST':
        from datetime import date
        deadline = request.form.get('deadline') or None
        p = Project(org_id=int(request.form.get('org_id')),
                    title=request.form.get('title','').strip(),
                    description=request.form.get('description','').strip(),
                    deadline=date.fromisoformat(deadline) if deadline else None)
        db.session.add(p); db.session.flush()
        for sid, md in zip(request.form.getlist('skill_ids'),
                           request.form.getlist('min_depths')):
            db.session.add(ProjectRequirement(
                project_id=p.project_id, skill_id=int(sid),
                min_depth=float(md or 50)))
        db.session.commit()
        flash('Project added!', 'success')
    projects = (db.session.query(Project, Organization,
            func.count(func.distinct(ProjectRequirement.skill_id)).label('req_count'))
        .join(Organization, Project.org_id == Organization.org_id)
        .outerjoin(ProjectRequirement, ProjectRequirement.project_id == Project.project_id)
        .group_by(Project.project_id, Organization.org_id)
        .order_by(Project.posted_at.desc()).all())
    return render_template('admin/projects.html',
        projects=projects, orgs=all_orgs, skills=all_skills)

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    full_report = (db.session.query(StudentSkill, User, Skill)
        .join(User,  StudentSkill.student_id == User.user_id)
        .join(Skill, StudentSkill.skill_id   == Skill.skill_id)
        .order_by(StudentSkill.risk_score.desc().nullslast()).all())
    student_summary = (db.session.query(User.username, User.branch,
            func.round(func.avg(StudentSkill.depth_score),1).label('avg_depth'),
            func.round(func.avg(StudentSkill.risk_score), 1).label('avg_risk'),
            func.count(StudentSkill.skill_id).label('skills'))
        .join(StudentSkill, StudentSkill.student_id == User.user_id)
        .filter(User.role=='Student')
        .group_by(User.user_id, User.username, User.branch)
        .order_by(func.avg(StudentSkill.risk_score).desc().nullslast()).all())
    high_risk_skills = (db.session.query(Skill, RiskParam)
        .join(RiskParam, RiskParam.skill_id == Skill.skill_id)
        .order_by((RiskParam.repetitiveness + RiskParam.ai_threat_level
                   - RiskParam.complexity/2.0).desc()).all())
    return render_template('admin/analytics.html',
        full_report=full_report, student_summary=student_summary,
        high_risk_skills=high_risk_skills)

@admin_bp.route('/export/csv')
@login_required
@admin_required
def export_csv():
    rows = (db.session.query(StudentSkill, User, Skill)
        .join(User,  StudentSkill.student_id == User.user_id)
        .join(Skill, StudentSkill.skill_id   == Skill.skill_id)
        .order_by(User.username).all())
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(['Username','Branch','Skill','Category','Depth','Risk','Level'])
    for ss, u, s in rows:
        w.writerow([u.username, u.branch or '', s.name, s.category,
                    float(ss.depth_score), float(ss.risk_score or 0), ss.risk_level])
    resp = make_response(out.getvalue())
    resp.headers['Content-Disposition'] = 'attachment; filename=stratos_report.csv'
    resp.headers['Content-Type'] = 'text/csv'
    return resp
