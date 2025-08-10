# backend/utils/auth_decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorator to ensure the user is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Please log in first", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    """Decorator to ensure the user has a specific role."""
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("role") != role:
                flash("Unauthorized access", "danger")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
