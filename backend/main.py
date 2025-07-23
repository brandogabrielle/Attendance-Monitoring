import pandas as pd

# Specify the correct path to your Excel file
file_path = "backend/generated_student_data.xlsx"

# Read the Excel file
df = pd.read_excel(file_path)

# Display the first 10 rows
print(df.head(10))
