from flask import Blueprint

ciudadano_bp = Blueprint("ciudadano", __name__, url_prefix="/ciudadano")

from . import routes
