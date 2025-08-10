# backend/routes/faculty.py
from flask import Blueprint, render_template, request
from datetime import datetime
import pandas as pd
import os

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

@faculty_bp.route('/')
def faculty_dashboard():
    faculty_id = request.args.get('faculty_id')
    section = request.args.get('section')
    subject = request.args.get('subject')
    faculty_name = request.args.get('name', 'Faculty User')  # optional

    return render_template(
        'faculty_dashboard.html',
        faculty_id=faculty_id,
        faculty_name=faculty_name,
        section=section,
        subject=subject
    )

@faculty_bp.route('/attend', methods=['POST'])
def faculty_attend():
    data = request.get_json()
    if not data:
        return "❌ Invalid request data", 400

    student_id = data.get('student_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    class_section = data.get('class_section')
    subject = data.get('subject')
    faculty_id = data.get('faculty_id')

    if not all([student_id, first_name, last_name, class_section, subject, faculty_id]):
        return "❌ Missing fields", 400

    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_dir, 'generated_student_data.xlsx')

    if not os.path.exists(excel_path):
        return "❌ Student data file not found", 500

    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        return f"❌ Error reading student data: {str(e)}", 500

    df.columns = df.columns.str.strip().str.lower()

    matched = df[
        (df['student_id'].astype(str) == str(student_id)) &
        (df['first_name'].str.lower() == first_name.lower()) &
        (df['last_name'].str.lower() == last_name.lower())
    ]

    if not matched.empty:
        timestamp = datetime.now().isoformat()
        attendance_record = {
            "student_id": student_id,
            "first_name": first_name,
            "last_name": last_name,
            "timestamp": timestamp,
            "class_section": class_section,
            "subject": subject,
            "faculty_id": faculty_id
        }

        log_file = os.path.join(base_dir, 'attendance_log.csv')
        df_attendance = pd.DataFrame([attendance_record])
        df_attendance.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)

        return f"✅ Attendance recorded for {first_name.title()} {last_name.title()}"
    else:
        return "❌ Student not found", 404
