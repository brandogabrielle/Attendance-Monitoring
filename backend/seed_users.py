# backend/seed_users.py

from werkzeug.security import generate_password_hash
import psycopg2

# Update this with your DB connection info
conn = psycopg2.connect(
    dbname="attendance_system",
    user="postgres",
    password="chicken018",  # 👈 replace with your postgres password
    host="localhost"
)
cur = conn.cursor()

# Clear old users
cur.execute("DELETE FROM users;")

# Insert users with hashed passwords
users = [
    ("admin1", generate_password_hash("admin123"), "Admin"),
    ("registrar1", generate_password_hash("reg123"), "Registrar"),
    ("faculty1", generate_password_hash("fac123"), "Faculty"),
]

for username, hashed_pw, role in users:
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, hashed_pw, role)
    )

conn.commit()
cur.close()
conn.close()

print("✅ Users seeded successfully with hashed passwords!")
