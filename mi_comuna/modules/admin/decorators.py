from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from . import admin_bp
from mi_comuna.modules.negocios.models import Negocio
from mi_comuna.modules.inicio.models import Noticia, Aviso, Evento
from mi_comuna.extensions import db

# Decorador admin
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != "admin":
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    stats = {
        "negocios": Negocio.query.count(),
        "noticias": Noticia.query.count(),
        "avisos": Aviso.query.count(),
        "eventos": Evento.query.count()
    }
    return render_template("admin/dashboard.html", stats=stats)


@admin_bp.route("/negocios")
@login_required
@admin_required
def negocios():
    negocios = Negocio.query.all()
    return render_template("admin/negocios.html", negocios=negocios)


@admin_bp.route("/negocios/<int:id>/aprobar")
@login_required
@admin_required
def aprobar_negocio(id):
    negocio = Negocio.query.get_or_404(id)
    negocio.estado = "aprobado"
    db.session.commit()
    flash("✅ Negocio aprobado", "success")
    return redirect(url_for("admin.negocios"))


@admin_bp.route("/negocios/<int:id>/desactivar")
@login_required
@admin_required
def desactivar_negocio(id):
    negocio = Negocio.query.get_or_404(id)
    negocio.estado = "pendiente"
    db.session.commit()
    flash("⚠️ Negocio desactivado", "warning")
    return redirect(url_for("admin.negocios"))
