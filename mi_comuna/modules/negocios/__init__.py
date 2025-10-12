from flask import Blueprint

negocios_bp = Blueprint(
    "negocios",
    __name__,
    template_folder="templates",
    static_folder="../static",  # Apunta a la carpeta 'static' en la raíz del proyecto
    url_prefix="/negocios",
)

from . import routes  # noqa: E402,F401
