from flask import Blueprint, request, jsonify
from models.user_model import get_user_by_username
from utils.auth_helpers import check_password  # ✅ RE-ENABLE THIS

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = get_user_by_username(username)
    if not user or user['role'] != role:
        return jsonify({'error': 'Invalid username or role'}), 401

    # ✅ USE SECURE PASSWORD CHECK NOW
    if not check_password(password, user['password']):
        return jsonify({'error': 'Incorrect password'}), 401

    return jsonify({
        'message': 'Login successful',
        'role': user['role'],
        'username': user['username']
    })
