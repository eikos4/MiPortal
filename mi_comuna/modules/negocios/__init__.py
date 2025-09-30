from flask import Blueprint

negocios_bp = Blueprint(
    "negocios", __name__,
    template_folder="templates",
    static_folder="static"
)

from . import routes
