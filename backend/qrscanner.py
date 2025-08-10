from flask import Flask, request, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/faculty/dashboard')
def faculty_dashboard():
    # Replace these with actual logged-in faculty info in your app
    faculty_info = {
        "faculty_name": "Dr. Smith",
        "faculty_id": "F123",
        "section": "Section A",
        "subject": "Math"
    }
    return render_template('faculty_dashboard.html', **faculty_info)

@app.route('/faculty/attend', methods=['POST'])
def attend():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid request data"}), 400

    student_id = data.get('student_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not all([student_id, first_name, last_name]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    # Build absolute path to Excel file
    excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generated_student_data.xlsx')

    if not os.path.exists(excel_path):
        return jsonify({"status": "error", "message": "Student data file not found"}), 500

    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error reading student data: {str(e)}"}), 500

    # Normalize columns
    df.columns = df.columns.str.strip().str.lower()

    # Validate student info
    matched = df[
        (df['student_id'].astype(str) == str(student_id)) &
        (df['first_name'].str.lower() == first_name.lower()) &
        (df['last_name'].str.lower() == last_name.lower())
    ]

    if not matched.empty:
        student = matched.iloc[0]
        return jsonify({
            "status": "success",
            "message": f"Attendance recorded for {student['first_name'].title()} {student['last_name'].title()}"
        })

    return jsonify({"status": "error", "message": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
