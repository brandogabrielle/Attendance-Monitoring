# backend/auth/routes.py

from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from backend.models.user_model import get_user_by_username
from backend.utils.auth_helpers import check_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Render a simple login form for testing
        return render_template('login.html')

    # POST request (login attempt)
    data = request.form if request.form else request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = get_user_by_username(username)
    if not user or user['role'] != role:
        return jsonify({'error': 'Invalid username or role'}), 401

    if not check_password(password, user['password']):
        return jsonify({'error': 'Incorrect password'}), 401

    # Save login info in session
    session['username'] = user['username']
    session['role'] = user['role']

    # Redirect based on role
    if user['role'] == 'faculty':
        return redirect(url_for('faculty.faculty_dashboard'))
    elif user['role'] == 'admin':
        return redirect(url_for('admin.admin_dashboard'))

    return jsonify({'message': 'Login successful but no role dashboard found'})

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
