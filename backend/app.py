from flask import Flask
from backend.auth.routes import auth_bp
from backend.routes.admin import admin_bp
from backend.routes.faculty import faculty_bp
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret-key")

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(faculty_bp)

if __name__ == "__main__":
    app.run(debug=True)
