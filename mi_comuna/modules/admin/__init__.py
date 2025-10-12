# mi_comuna/modules/admin/__init__.py
from flask import Blueprint

admin_bp = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    static_folder="../static",
    url_prefix="/admin",
)

# Importa rutas al final para evitar ciclos
from . import routes  # noqa: E402,F401
