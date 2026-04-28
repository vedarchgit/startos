from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, limiter
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET','POST'])
@limiter.limit("20 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        if not username or not password:
            flash('Fill in all fields.', 'danger')
            return render_template('login.html')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=request.form.get('remember')=='on')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET','POST'])
@limiter.limit("10 per minute")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    data = {}
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        email    = request.form.get('email','').strip().lower()
        password = request.form.get('password','')
        branch   = request.form.get('branch','').strip() or None
        year     = request.form.get('year') or None
        data = dict(username=username, email=email, branch=branch, year=year)

        errors = []
        if len(username) < 3:      errors.append('Username must be ≥3 chars.')
        if '@' not in email:       errors.append('Enter a valid email.')
        if len(password) < 8:      errors.append('Password must be ≥8 chars.')
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken.')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')

        if errors:
            for e in errors: flash(e, 'danger')
            return render_template('register.html', **data)

        u = User(username=username, email=email,
                 password=generate_password_hash(password),
                 role='Student', branch=branch,
                 year=int(year) if year else None)
        db.session.add(u)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', **data)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('auth.login'))
