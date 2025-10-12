from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    """Permite solo administradores."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Debes iniciar sesión para acceder.", "warning")
            return redirect(url_for("auth.login"))
        if current_user.rol != "admin":
            flash("🚫 No tienes permisos para acceder al panel de administración.", "danger")
            return redirect(url_for("inicio.index"))
        return f(*args, **kwargs)
    return decorated_function
