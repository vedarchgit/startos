from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import StudentSkill, Skill, LabTask, TaskAttempt, Project
from utils.depth import recalculate_depth, student_eligible_for_project

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_only(f):
    @wraps(f)
    def dec(*a, **kw):
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return f(*a, **kw)
    return dec

@student_bp.route('/dashboard')
@login_required
@student_only
def dashboard():
    my_skills = (db.session.query(StudentSkill, Skill)
        .join(Skill, StudentSkill.skill_id == Skill.skill_id)
        .filter(StudentSkill.student_id == current_user.user_id)
        .order_by(StudentSkill.risk_score.desc().nullslast()).all())

    eligible_projects = []
    for p in Project.query.all():
        ok, _ = student_eligible_for_project(current_user.user_id, p.project_id)
        if ok:
            eligible_projects.append(p)

    recent = (db.session.query(TaskAttempt, LabTask, Skill)
        .join(LabTask, TaskAttempt.task_id == LabTask.task_id)
        .join(Skill,   LabTask.skill_id    == Skill.skill_id)
        .filter(TaskAttempt.student_id == current_user.user_id)
        .order_by(TaskAttempt.attempted_at.desc()).limit(5).all())

    return render_template('student/dashboard.html',
        my_skills=my_skills, eligible_projects=eligible_projects, recent=recent)

@student_bp.route('/tasks')
@login_required
@student_only
def view_tasks():
    tasks = (db.session.query(LabTask, Skill)
        .join(Skill, LabTask.skill_id == Skill.skill_id)
        .order_by(Skill.name, LabTask.difficulty).all())
    return render_template('student/tasks.html', tasks=tasks)

@student_bp.route('/attempt/<int:task_id>', methods=['POST'])
@login_required
@student_only
def submit_attempt(task_id):
    task = db.session.get(LabTask, task_id)
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('student.view_tasks'))
    try:
        score = float(request.form.get('score',''))
        assert 0 <= score <= float(task.max_score)
    except (ValueError, AssertionError):
        flash(f'Score must be 0–{task.max_score}.', 'danger')
        return redirect(url_for('student.view_tasks'))

    db.session.add(TaskAttempt(student_id=current_user.user_id,
                                task_id=task_id, score_achieved=score))
    db.session.flush()
    new_depth = recalculate_depth(current_user.user_id, task.skill_id)
    flash(f'Score {score:.0f} recorded! {task.skill.name} depth → {new_depth:.1f}%', 'success')
    return redirect(url_for('student.dashboard'))

@student_bp.route('/apply/<int:project_id>', methods=['POST'])
@login_required
@student_only
def apply_project(project_id):
    p = db.session.get(Project, project_id)
    if not p:
        flash('Project not found.', 'danger')
        return redirect(url_for('student.dashboard'))
    ok, missing = student_eligible_for_project(current_user.user_id, project_id)
    if not ok:
        flash('Not eligible: ' + ', '.join(missing), 'warning')
        return redirect(url_for('student.dashboard'))
    if current_user in p.students:
        flash('Already applied.', 'info')
        return redirect(url_for('student.dashboard'))
    p.students.append(current_user)
    db.session.commit()
    flash(f'Applied to "{p.title}"!', 'success')
    return redirect(url_for('student.dashboard'))

@student_bp.route('/report')
@login_required
@student_only
def risk_report():
    report = (db.session.query(StudentSkill, Skill)
        .join(Skill, StudentSkill.skill_id == Skill.skill_id)
        .filter(StudentSkill.student_id == current_user.user_id)
        .order_by(StudentSkill.risk_score.desc().nullslast()).all())
    return render_template('student/report.html', report=report)
