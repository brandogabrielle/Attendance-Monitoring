# backend/routes/faculty.py
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import os
import time

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

# Store recent scans for cooldown
recent_scans = {}
scan_history = []
COOLDOWN_SECONDS = 5  # seconds between allowed duplicate scans

# Absolute path to the Excel file
excel_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'generated_student_data.xlsx')

@faculty_bp.route('/dashboard')
def faculty_dashboard():
    return render_template(
        'faculty_dashboard.html',
        faculty_id=request.args.get('faculty_id'),
        faculty_name=request.args.get('name', 'Faculty User'),
        section=request.args.get('section'),
        subject=request.args.get('subject')
    )

@faculty_bp.route('/attend', methods=['POST'])
def attend():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid request data"}), 400

    student_id = str(data.get('student_id')).strip()
    now = time.time()

    if not student_id:
        return jsonify({"status": "error", "message": "Missing student ID"}), 400

    # Cooldown check per student
    if student_id in recent_scans and now - recent_scans[student_id] < COOLDOWN_SECONDS:
        scan_history.insert(0, (time.strftime('%I:%M:%S %p'), student_id, "Duplicate Scan", "cooldown"))
        scan_history[:] = scan_history[:5]
        return jsonify({
            "status": "cooldown",
            "message": "⏳ Duplicate scan ignored (cooldown)",
            "recent_scans": scan_history
        }), 429

    # Check if Excel exists
    if not os.path.exists(excel_path):
        return jsonify({"status": "error", "message": "Student data file not found"}), 500

    try:
        df = pd.read_excel(excel_path)
        df.columns = df.columns.str.strip().str.lower()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error reading student data: {str(e)}"}), 500

    matched = df[df['student_id'].astype(str) == student_id]

    if not matched.empty:
        student = matched.iloc[0]
        student_name = f"{student['first_name'].title()} {student['last_name'].title()}"
        recent_scans[student_id] = now
        scan_history.insert(0, (time.strftime('%I:%M:%S %p'), student_id, student_name, "success"))
        scan_history[:] = scan_history[:5]
        return jsonify({
            "status": "success",
            "message": f"✅ Attendance recorded for {student_name}",
            "recent_scans": scan_history
        })

    # If not found
    recent_scans[student_id] = now
    scan_history.insert(0, (time.strftime('%I:%M:%S %p'), student_id, "Unknown", "error"))
    scan_history[:] = scan_history[:5]
    return jsonify({
        "status": "error",
        "message": "❌ Student not found",
        "recent_scans": scan_history
    }), 404
