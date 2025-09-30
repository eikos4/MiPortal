from flask import Blueprint

ciudadano_bp = Blueprint(
    "ciudadano",
    __name__,
    url_prefix="/ciudadano",
    template_folder="templates"
)
