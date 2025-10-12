from flask import Blueprint

inicio_bp = Blueprint(
    "inicio", __name__,
    template_folder="templates",
    static_folder="../static",
    url_prefix="/"
)

from . import routes
