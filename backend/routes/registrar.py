from flask import Blueprint, render_template, session
from backend.utils.auth_decorators import role_required

registrar_bp = Blueprint('registrar', __name__, url_prefix='/registrar')

@registrar_bp.route('/')
@role_required('registrar')
def registrar_dashboard():
    return render_template('registrar_dashboard.html', username=session['username'])
