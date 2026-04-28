"""
routes/api.py — JSON API endpoints for Chart.js charts
"""

from flask       import Blueprint, jsonify
from flask_login import login_required, current_user
from extensions  import db
from models      import StudentSkill, Skill, RiskParam, TaskAttempt, LabTask, User
from sqlalchemy  import func

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/my-risk')
@login_required
def my_risk():
    """Student's own skill depth vs risk — used in student dashboard chart."""
    rows = (
        db.session.query(StudentSkill, Skill)
        .join(Skill, StudentSkill.skill_id == Skill.skill_id)
        .filter(StudentSkill.student_id == current_user.user_id)
        .order_by(StudentSkill.risk_score.desc().nullslast())
        .all()
    )
    return jsonify([{
        'skill':      s.name,
        'depth':      float(ss.depth_score or 0),
        'risk':       float(ss.risk_score  or 0),
        'risk_level': ss.risk_level,
    } for ss, s in rows])


@api_bp.route('/skill-risk-overview')
@login_required
def skill_risk_overview():
    """Admin: average risk per skill across all students."""
    rows = (
        db.session.query(
            Skill.name,
            func.round(func.avg(StudentSkill.risk_score), 1).label('avg_risk'),
            func.round(func.avg(StudentSkill.depth_score), 1).label('avg_depth'),
            func.count(StudentSkill.student_id).label('student_count'),
        )
        .join(StudentSkill, StudentSkill.skill_id == Skill.skill_id)
        .group_by(Skill.skill_id, Skill.name)
        .order_by(func.avg(StudentSkill.risk_score).desc().nullslast())
        .all()
    )
    return jsonify([{
        'skill':         r.name,
        'avg_risk':      float(r.avg_risk  or 0),
        'avg_depth':     float(r.avg_depth or 0),
        'student_count': r.student_count,
    } for r in rows])


@api_bp.route('/attempts-over-time')
@login_required
def attempts_over_time():
    """Admin: daily attempt counts for the last 30 days."""
    from datetime import date, timedelta
    rows = (
        db.session.query(
            func.date(TaskAttempt.attempted_at).label('day'),
            func.count(TaskAttempt.attempt_id).label('cnt'),
        )
        .filter(TaskAttempt.attempted_at >= date.today() - timedelta(days=30))
        .group_by(func.date(TaskAttempt.attempted_at))
        .order_by(func.date(TaskAttempt.attempted_at))
        .all()
    )
    return jsonify([{'day': str(r.day), 'count': r.cnt} for r in rows])


@api_bp.route('/base-risk-scores')
@login_required
def base_risk_scores():
    """All skills with their base risk score (no student context)."""
    rows = (
        db.session.query(Skill, RiskParam)
        .join(RiskParam, RiskParam.skill_id == Skill.skill_id)
        .order_by(
            (RiskParam.repetitiveness + RiskParam.ai_threat_level
             - RiskParam.complexity / 2.0).desc()
        )
        .all()
    )
    return jsonify([{
        'skill':            s.name,
        'category':         s.category,
        'base_risk':        rp.base_risk_score,
        'repetitiveness':   rp.repetitiveness,
        'ai_threat_level':  rp.ai_threat_level,
        'complexity':       rp.complexity,
    } for s, rp in rows])
