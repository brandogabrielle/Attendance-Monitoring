from flask import Flask, request, jsonify, render_template
import pandas as pd
from flask import request


app = Flask(__name__)

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

    student_id = data.get('student_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not all([student_id, first_name, last_name]):
        return "❌ Missing fields", 400

    # Load and sanitize Excel data
    df = pd.read_excel('generated_student_data.xlsx')
    df.columns = df.columns.str.strip().str.lower()

    print("📋 First 5 students in Excel:")
    print(df.head())

    # Match by lowercased comparison
    matched = df[
        (df['student_id'].astype(str) == str(student_id)) &
        (df['first_name'].str.lower() == first_name.lower()) &
        (df['last_name'].str.lower() == last_name.lower())
    ]

    if not matched.empty:
        print("✅ Match found:", matched.iloc[0].to_dict())
        return f"✅ Attendance recorded for {first_name.title()} {last_name.title()}"
    else:
        print("❌ No match found for:", data)
        return "❌ Student not found", 404

if __name__ == '__main__':
    app.run(debug=True)
