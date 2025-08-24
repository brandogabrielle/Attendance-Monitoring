from flask import Blueprint, render_template, session
from backend.utils.auth_decorators import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@role_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html', username=session['username'])
