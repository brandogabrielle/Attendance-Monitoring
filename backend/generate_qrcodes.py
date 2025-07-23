import pandas as pd
import qrcode
import json
import os

#read student data from Excel file
df = pd.read_excel("backend/generated_student_data.xlsx")
df.columns = df.columns.str.strip().str.lower()

#create output directory if it doesn't exist
output_dir = "backend/qr_codes"

os.makedirs(output_dir, exist_ok=True)

#loop through each student in the DataFrame

for index, row in df.iterrows():
    student = {
        "student_id": row["student_id"],
        "last_name": row["last_name"],
        "first_name": row["first_name"]
    }

    filename = f"{row['last_name']}_{row['student_id']}_qr.png"
    #convert student info to JSON
    qr_data = json.dumps(student)

    #generate QR code
    qr = qrcode.make(qr_data)

    #save QR code as an image file
    qr_file_path = os.path.join(output_dir, f"{row['student_id']}_qr.png")
    qr.save(qr_file_path)
    print(f"QR code generated and saved as {qr_file_path}")

    print(f"QR code for {row['first_name']} {row['last_name']} generated successfully.")
# This script reads student data from an Excel file and generates QR codes for each student.