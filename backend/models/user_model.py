# Simulated users for now
users = [
    {'username': 'juanfaculty', 'password': '$2b$12$abc...', 'role': 'faculty'},
    {'username': 'mariaadmin', 'password': '$2b$12$def...', 'role': 'admin'}
]

def get_user_by_username(username):
    for user in users:
        if user['username'] == username:
            return user
    return None
