from flask import Flask
from auth.routes import auth_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows all domains by default

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace in production

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
