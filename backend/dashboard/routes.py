# backend/dashboard/routes.py
from flask import Blueprint, session, redirect, url_for

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
