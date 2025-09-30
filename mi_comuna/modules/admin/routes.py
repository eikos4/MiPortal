from flask import render_template, redirect, request, url_for, flash
from . import admin_bp
from mi_comuna.modules.negocios.models import Negocio
from mi_comuna.modules.inicio.models import Noticia, Aviso, Evento
from mi_comuna.extensions import db
from flask_login import login_required
from .decorators import admin_required
from datetime import datetime


# ============================
# Dashboard
# ============================
@admin_bp.route("/")
@login_required
@admin_required
def admin_dashboard():
    """Dashboard con métricas generales"""
    stats = {
        "negocios": Negocio.query.count(),
        "noticias": Noticia.query.count(),
        "avisos": Aviso.query.count(),
        "eventos": Evento.query.count()
    }
    return render_template("admin/dashboard.html", stats=stats)


# ============================
# Negocios
# ============================
@admin_bp.route("/negocios")
@login_required
@admin_required
def admin_negocios():
    negocios = Negocio.query.all()
    return render_template("admin/negocios.html", negocios=negocios)


@admin_bp.route("/negocios/<int:id>/aprobar")
@login_required
@admin_required
def admin_aprobar_negocio(id):
    negocio = Negocio.query.get_or_404(id)
    negocio.estado = "aprobado"
    db.session.commit()
    flash("✅ Negocio aprobado con éxito", "success")
    return redirect(url_for("admin.admin_negocios"))


@admin_bp.route("/negocios/<int:id>/desactivar")
@login_required
@admin_required
def admin_desactivar_negocio(id):
    negocio = Negocio.query.get_or_404(id)
    negocio.estado = "pendiente"
    db.session.commit()
    flash("⚠️ Negocio desactivado", "warning")
    return redirect(url_for("admin.admin_negocios"))



@admin_bp.route("/negocios/<int:id>/eliminar")
@login_required
@admin_required
def admin_eliminar_negocio(id):
    negocio = Negocio.query.get_or_404(id)
    db.session.delete(negocio)
    db.session.commit()
    flash("🗑️ Negocio eliminado con éxito", "warning")
    return redirect(url_for("admin.admin_negocios"))


# ============================
# Noticias
# ============================
@admin_bp.route("/noticias")
@login_required
@admin_required
def admin_noticias():
    noticias = Noticia.query.order_by(Noticia.id.desc()).all()
    return render_template("admin/noticias.html", noticias=noticias)


@admin_bp.route("/noticias/crear", methods=["GET", "POST"])
@login_required
@admin_required
def admin_crear_noticia():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        contenido = request.form.get("contenido")

        nueva = Noticia(
            titulo=titulo,
            contenido=contenido,
            fecha=datetime.utcnow()   # 👈 Agregamos la fecha actual
        )

        db.session.add(nueva)
        db.session.commit()
        flash("📰 Noticia creada con éxito", "success")
        return redirect(url_for("admin.admin_noticias"))

    return render_template("admin/crear_noticia.html")


@admin_bp.route("/noticias/<int:id>/eliminar", endpoint="eliminar_noticia")
@login_required
@admin_required
def admin_eliminar_noticia(id):
    noticia = Noticia.query.get_or_404(id)
    db.session.delete(noticia)
    db.session.commit()
    flash("🗑️ Noticia eliminada", "warning")
    return redirect(url_for("admin.admin_noticias"))


# ============================
# Avisos
# ============================
@admin_bp.route("/avisos")
@login_required
@admin_required
def admin_avisos():
    avisos = Aviso.query.order_by(Aviso.id.desc()).all()
    return render_template("admin/avisos.html", avisos=avisos)


@admin_bp.route("/avisos/crear", methods=["GET", "POST"])
@login_required
@admin_required
def admin_crear_aviso():
    if request.method == "POST":
        mensaje = request.form.get("mensaje")
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")

        nuevo = Aviso(
            mensaje=mensaje,
            fecha_inicio=datetime.strptime(fecha_inicio, "%Y-%m-%d"),
            fecha_fin=datetime.strptime(fecha_fin, "%Y-%m-%d"),
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("📢 Aviso creado con éxito", "success")
        return redirect(url_for("admin.admin_avisos"))
    return render_template("admin/crear_aviso.html")


@admin_bp.route("/avisos/<int:id>/eliminar", endpoint="eliminar_aviso")
@login_required
@admin_required
def admin_eliminar_aviso(id):
    aviso = Aviso.query.get_or_404(id)
    db.session.delete(aviso)
    db.session.commit()
    flash("🗑️ Aviso eliminado", "warning")
    return redirect(url_for("admin.admin_avisos"))


# ============================
# Eventos
# ============================
@admin_bp.route("/eventos")
@login_required
@admin_required
def admin_eventos():
    eventos = Evento.query.order_by(Evento.fecha.asc()).all()
    return render_template("admin/eventos.html", eventos=eventos, now=datetime.utcnow)


@admin_bp.route("/eventos/crear", methods=["GET", "POST"])
@login_required
@admin_required
def admin_crear_evento():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        lugar = request.form.get("lugar")
        fecha = request.form.get("fecha")

        nuevo = Evento(
            titulo=titulo,
            lugar=lugar,
            fecha=datetime.strptime(fecha, "%Y-%m-%d"),
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("🎉 Evento creado con éxito", "success")
        return redirect(url_for("admin.admin_eventos"))
    return render_template("admin/crear_evento.html")


@admin_bp.route("/eventos/<int:id>/editar", methods=["GET", "POST"])
@login_required
@admin_required
def admin_editar_evento(id):
    evento = Evento.query.get_or_404(id)
    if request.method == "POST":
        evento.titulo = request.form.get("titulo")
        evento.lugar = request.form.get("lugar")
        evento.fecha = datetime.strptime(request.form.get("fecha"), "%Y-%m-%d")
        db.session.commit()
        flash("✏️ Evento actualizado con éxito", "success")
        return redirect(url_for("admin.admin_eventos"))
    return render_template("admin/editar_evento.html", evento=evento)


@admin_bp.route("/eventos/<int:id>/eliminar")
@login_required
@admin_required
def admin_eliminar_evento(id):
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    flash("🗑️ Evento eliminado", "warning")
    return redirect(url_for("admin.admin_eventos"))
