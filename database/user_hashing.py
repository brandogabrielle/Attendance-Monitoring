# database/user_service.py (or wherever you handle user creation)

from werkzeug.security import generate_password_hash
from database.db import get_db

def create_user(username, raw_password, role):
    """
    Creates a new user with a hashed password.
    """
    db = get_db()
    cursor = db.cursor()

    # Hash the raw password
    hashed_pw = generate_password_hash(raw_password)

    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hashed_pw, role)
    )

    db.commit()
    print(f"✅ User '{username}' created with role '{role}' (password hashed).")
