from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
plain_password = "admin018"
hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

print(f"Hashed password for 'admin018': {hashed_password}")
