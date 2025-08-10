# backend/routes/admin.py
from flask import Blueprint, render_template, request

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_dashboard():
    admin_name = request.args.get('name', 'Admin User')
    return render_template(
        'admin_dashboard.html',
        admin_name=admin_name
    )
