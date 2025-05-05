from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

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