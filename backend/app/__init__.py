from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

# Load environment variables from both root and app directory
load_dotenv()  # Load from root directory
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))  # Load from app directory

# Initialize extensions
ma = Marshmallow()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configure the Flask application
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')
    
    # Initialize CORS
    CORS(app)
    
    # Initialize extensions with app
    ma.init_app(app)
    
    # Register blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app 