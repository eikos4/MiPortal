from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def ciudadano_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Debes iniciar sesión para acceder.", "warning")
            return redirect(url_for("auth.login"))
        if current_user.rol != "ciudadano":
            flash("🚫 Solo los ciudadanos pueden acceder aquí.", "danger")
            return redirect(url_for("inicio.index"))
        return f(*args, **kwargs)
    return decorated_function
