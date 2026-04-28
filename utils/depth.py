"""
utils/depth.py
Depth + risk recalculation in Python, not SQL triggers.
Reason: SQLAlchemy ORM session doesn't see trigger-updated rows without
a fresh query — causes stale data on the dashboard after submission.
"""
from extensions import db


def recalculate_depth(student_id: int, skill_id: int) -> float:
    """
    Recompute depth_score for one student-skill pair.
    Formula: AVG( (score / max_score) * difficulty_weight ) * 100
    Hard tasks (weight=2.0) count more than Easy (weight=0.5).
    """
    from models import TaskAttempt, LabTask, StudentSkill

    rows = (
        db.session.query(TaskAttempt, LabTask)
        .join(LabTask, TaskAttempt.task_id == LabTask.task_id)
        .filter(TaskAttempt.student_id == student_id, LabTask.skill_id == skill_id)
        .all()
    )

    if not rows:
        return 0.0

    total = sum(
        (float(a.score_achieved) / float(t.max_score)) * float(t.difficulty_weight)
        for a, t in rows
    )
    depth = round((total / len(rows)) * 100, 2)

    ss = db.session.get(StudentSkill, (student_id, skill_id))
    if ss is None:
        ss = StudentSkill(student_id=student_id, skill_id=skill_id)
        db.session.add(ss)

    ss.depth_score = depth
    ss.recalculate_risk()
    db.session.commit()
    return depth


def student_eligible_for_project(student_id: int, project_id: int):
    """Returns (eligible: bool, missing: list[str])"""
    from models import ProjectRequirement, StudentSkill, Skill

    reqs = (
        db.session.query(ProjectRequirement, Skill)
        .join(Skill, ProjectRequirement.skill_id == Skill.skill_id)
        .filter(ProjectRequirement.project_id == project_id)
        .all()
    )
    missing = []
    for req, skill in reqs:
        ss = db.session.get(StudentSkill, (student_id, req.skill_id))
        depth = float(ss.depth_score) if ss else 0.0
        if depth < float(req.min_depth):
            missing.append(f"{skill.name} (need {float(req.min_depth):.0f}%, have {depth:.0f}%)")
    return (len(missing) == 0, missing)
