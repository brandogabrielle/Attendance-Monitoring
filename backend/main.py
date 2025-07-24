from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
import json

app = Flask(__name__)

# Load the Excel file once
df = pd.read_excel("/Users/brandogabrielle/Documents/Capstone/Attendance-Monitoring/backend/generated_student_data.xlsx")

@app.route('/')
def index():
    return render_template('scanner.html')  # This will load your scanner page

@app.route('/attend', methods=['POST'])
def attend():
    data = request.json
    print("Received data:", data)  # 👈 Add this line to see what's coming in

    student_id = data.get("student_id")
    last_name = data.get("last_name")
    first_name = data.get("first_name")

    if student_id is None or last_name is None or first_name is None:
        return jsonify({"status": "error", "message": "Incomplete data"}), 400

    # ... rest of the code stays the same ...

    match = df[
        (df['student_id'].astype(str).str.strip() == str(student_id).strip()) &
        (df['last_name'].str.lower().str.strip() == last_name.lower().strip()) &
        (df['first_name'].str.lower().str.strip() == first_name.lower().strip())
    ]

    if not match.empty:
        return jsonify({"status": "success", "message": "Attendance recorded!"})
    else:
        return jsonify({"status": "error", "message": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

#use this to run the app python /Users/brandogabrielle/Documents/Capstone/Attendance-Monitoring/backend/main.py
