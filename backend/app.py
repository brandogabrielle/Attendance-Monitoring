from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

faculty_data = {
    1: {
        "name": "Prof. John Smith",
        "subjects": {
            "BSIT 3A": ["Data Structures", "Networking Basics"],
            "BSIT 3B": ["Operating Systems"]
        }
    },
    2: {
        "name": "Prof. Jane Doe",
        "subjects": {
            "BSCS 2A": ["Introduction to Programming"]
        }
    }
}

@app.route('/')
@app.route('/select_class')
def select_class():
    return render_template('select_class.html', faculty_data=faculty_data)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scan')
def scan():
    faculty_id = request.args.get('faculty')
    section = request.args.get('section')
    subject = request.args.get('subject')
    return render_template('scanner.html', faculty_id=faculty_id, section=section, subject=subject)

@app.route('/attend', methods=['POST'])
def attend():
    data = request.get_json()
    if not data:
        return "❌ Invalid request data", 400

    # 🧾 Extract student info
    student_id = data.get('student_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # ✅ Extract context info
    class_section = data.get('class_section')
    subject = data.get('subject')
    faculty_id = data.get('faculty_id')

    # 🛡 Validate everything is present
    if not all([student_id, first_name, last_name, class_section, subject, faculty_id]):
        return "❌ Missing fields or context", 400

    # 🔎 Load masterlist and match student
    df = pd.read_excel('generated_student_data.xlsx')
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

        # 📝 Save to CSV
        log_file = 'attendance_log.csv'
        df_attendance = pd.DataFrame([attendance_record])
        df_attendance.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)

        print("✅ Match recorded:", attendance_record)
        return f"✅ Attendance recorded for {first_name.title()} {last_name.title()}"

    else:
        print("❌ No match found for:", data)
        return "❌ Student not found", 404

@app.route('/records')
def records():
    try:
        df = pd.read_csv('attendance_log.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["student_id", "first_name", "last_name", "timestamp"])
    return render_template('records.html', data=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
