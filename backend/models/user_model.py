# Simulated users for now
users = [
    {'username': 'faculty01', 'password': '$2b$12$F/1df7EiDcMgsO6wj4KLTeQMwUBRbuX0QNrbk0z8cH0NlK85oARFy', 'role': 'faculty'},
    {'username': 'admin01', 'password': '$2b$12$B.on4E.Ds07sbS7fDJWGvOwZy/nB4UNTkHrQXrAEcx68LE.I2aC16', 'role': 'admin'}
]

def get_user_by_username(username):
    for user in users:
        if user['username'] == username:
            return user
    return None
