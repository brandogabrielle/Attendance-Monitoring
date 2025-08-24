from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint('dashboard', __name__)

# Role-based access decorator
def role_required(role):
    def wrapper(fn):
        def decorated_view(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('auth.login'))
            return fn(*args, **kwargs)
        decorated_view.__name__ = fn.__name__
        return decorated_view
    return wrapper

@dashboard_bp.route('/faculty')
@role_required('faculty')
def faculty_dashboard():
    return render_template('faculty_dashboard.html', username=session['username'])

@dashboard_bp.route('/admin')
@role_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html', username=session['username'])

@dashboard_bp.route('/registrar')
@role_required('registrar')
def registrar_dashboard():
    return render_template('registrar_dashboard.html', username=session['username'])