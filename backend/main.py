from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime

app = Flask(__name__)  # ← THIS is what's missing

# Load your student Excel file
df = pd.read_excel("/Users/brandogabrielle/Documents/Capstone/Attendance-Monitoring/backend/generated_student_data.xlsx")

# List to store attendance logs
attendance_log = []


@app.route('/attend', methods=['POST'])
def attend():
    data = request.get_json()

    try:
        student_id = str(data.get("student_id", "")).strip()
        last_name = str(data.get("last_name", "")).strip().lower()
        first_name = str(data.get("first_name", "")).strip().lower()

        # Ensure Excel is processed the same way
        df['student_id'] = df['student_id'].astype(str).str.strip()
        df['last_name'] = df['last_name'].astype(str).str.strip().str.lower()
        df['first_name'] = df['first_name'].astype(str).str.strip().str.lower()

        # Now match all fields
        student = df[
            (df['student_id'] == student_id) &
            (df['last_name'] == last_name) &
            (df['first_name'] == first_name)
        ]

        if student.empty:
            return "❌ Student not found", 404

        record = {
            "student_id": student_id,
            "name": f"{student.iloc[0]['last_name'].title()}, {student.iloc[0]['first_name'].title()}",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        attendance_log.append(record)
        print("✅ Attendance logged:", record)
        return f"✅ Attendance recorded for {record['name']}"

    except Exception as e:
        print("⚠️ Error during attendance check:", e)
        return "❌ Invalid input or server error", 500
