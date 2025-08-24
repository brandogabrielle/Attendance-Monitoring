# backend/auth/routes.py

from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from werkzeug.security import check_password_hash
from database.db import get_user_by_username

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Accept both form and JSON payloads
    data = request.form if request.form else (request.get_json(silent=True) or {})
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    role_input = data.get('role')  # may be None or different casing

    # Basic input guardrails
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = get_user_by_username(username)
    if not user:
        # keep message style consistent with your current API
        return jsonify({'error': 'Invalid username or role'}), 401

    # If a role was provided by the client, compare it case-insensitively
    if role_input:
        if user['role'].strip().casefold() != str(role_input).strip().casefold():
            return jsonify({'error': 'Invalid username or role'}), 401

    # Verify hashed password (DB stores a hash from generate_password_hash)
    if not check_password_hash(user['password'], password):
        return jsonify({'error': 'Incorrect password'}), 401

    # Persist session
    session['username'] = user['username']
    session['role'] = user['role']  # keep DB’s canonical value (e.g., Admin/Faculty/Registrar)

    # Redirect based on the user's DB role (case-insensitive)
    role_key = user['role'].strip().casefold()
    route_map = {
        'faculty': 'faculty.faculty_dashboard',
        'admin': 'admin.admin_dashboard',
        'registrar': 'registrar.registrar_dashboard',
    }
    if role_key in route_map:
        return redirect(url_for(route_map[role_key]))

    return jsonify({'message': 'Login successful but no role dashboard found'})

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
