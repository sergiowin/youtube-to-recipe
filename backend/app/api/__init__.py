from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import routes  # Import routes at the bottom to avoid circular imports 