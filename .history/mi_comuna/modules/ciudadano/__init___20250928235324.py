from flask import Blueprint

ciudadano_bp = Blueprint(
    "ciudadano",   # 👈 este es el nombre usado en url_for
    __name__,
    url_prefix="/ciudadano",
    template_folder="templates"
)

from . import routes
