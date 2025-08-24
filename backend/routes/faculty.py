# backend/routes/faculty.py
from flask import Blueprint, render_template, session, request, jsonify
from backend.utils.auth_decorators import role_required
import pandas as pd
import os
import time

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

@role_required('faculty')
def faculty_dashboard():
    return render_template('faculty_dashboard.html', username=session['username'])


# Attendance session state
current_session = {
    "subject": None,
    "section": None,
    "scanned_ids": set(),  # IDs scanned in this session
    "last_scanned_id": None
}

# Store recent scans for display
scan_history = []

# Absolute path to the Excel file
excel_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'generated_student_data.xlsx'
)

# Faculty dashboard
@faculty_bp.route('/dashboard')
def faculty_dashboard():
    return render_template(
        'faculty_dashboard.html',
        faculty_id=request.args.get('faculty_id'),
        faculty_name=request.args.get('name', 'Faculty User'),
        section=request.args.get('section'),
        subject=request.args.get('subject')
    )

# Start attendance session
@faculty_bp.route('/start_session', methods=['POST'])
def start_session():
    data = request.get_json()
    subject = data.get("subject")
    section = data.get("section")

    if not subject or not section:
        return jsonify({"status": "error", "message": "Subject and section are required"}), 400

    # Reset session state
    current_session["subject"] = subject
    current_session["section"] = section
    current_session["scanned_ids"].clear()
    current_session["last_scanned_id"] = None

    scan_history.clear()

    return jsonify({
        "status": "success",
        "message": f"Attendance started for {subject} - {section}"
    })

# Record attendance
@faculty_bp.route('/attend', methods=['POST'])
def attend():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid request data"}), 400

    student_id = str(data.get('student_id', '')).strip()
    subject = data.get("subject")
    section = data.get("section")

    if not student_id or not subject or not section:
        return jsonify({"status": "error", "message": "Missing required data"}), 400

    # Ensure a session is active
    if current_session["subject"] != subject or current_session["section"] != section:
        return jsonify({"status": "error", "message": "No active session for this subject/section"}), 400

    # 1️⃣ Ignore if same as last scanned QR (prevents camera spam)
    if student_id == current_session["last_scanned_id"]:
        return jsonify({"status": "ignored", "message": "Same QR as last scan", "recent_scans": scan_history}), 200

    # 2️⃣ Ignore if already scanned in this session
    if student_id in current_session["scanned_ids"]:
        return jsonify({"status": "ignored", "message": "Already scanned in this session", "recent_scans": scan_history}), 200

    # Load Excel
    if not os.path.exists(excel_path):
        return jsonify({"status": "error", "message": "Student data file not found"}), 500

    try:
        df = pd.read_excel(excel_path)
        df.columns = df.columns.str.strip().str.lower()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error reading student data: {str(e)}"}), 500

    # Ensure 'section' column exists
    if 'section' not in df.columns:
        return jsonify({"status": "error", "message": "Section column missing in Excel"}), 500

    # Match student in the correct section
    matched = df[
        (df['student_id'].astype(str) == student_id) &
        (df['section'].astype(str).str.lower() == section.lower())
    ]

    if not matched.empty:
        student = matched.iloc[0]
        student_name = f"{student['first_name'].title()} {student['last_name'].title()}"

        # Record attendance
        current_session["last_scanned_id"] = student_id
        current_session["scanned_ids"].add(student_id)

        scan_history.insert(0, (time.strftime('%I:%M:%S %p'), student_id, student_name, "success"))
        scan_history[:] = scan_history[:5]

        return jsonify({
            "status": "success",
            "message": f"✅ Attendance recorded for {student_name}",
            "recent_scans": scan_history
        })

    # Student not found in section
    current_session["last_scanned_id"] = student_id
    scan_history.insert(0, (time.strftime('%I:%M:%S %p'), student_id, "Unknown", "error"))
    scan_history[:] = scan_history[:5]
    return jsonify({
        "status": "error",
        "message": "❌ Student not found in this section",
        "recent_scans": scan_history
    }), 404
