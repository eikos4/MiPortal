# mi_comuna/modules/admin/routes.py
import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from mi_comuna.extensions import db
from . import admin_bp  # ← usa el bp que definiste en __init__
from mi_comuna.modules.admin.decorators import admin_required
from mi_comuna.modules.inicio.models import Noticia, Aviso, Evento
from mi_comuna.modules.negocios.models import Negocio, Categoria
from mi_comuna.modules.auth.models import Usuario

UPLOAD_FOLDER = os.path.join("mi_comuna", "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_image(file_storage):
    if not file_storage or file_storage.filename == "":
        return None
    filename = secure_filename(file_storage.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file_storage.save(path)
    return f"uploads/{filename}"

# ---------- Panel principal ----------
@admin_bp.route("/", methods=["GET"], endpoint="dashboard")
@login_required
@admin_required
def dashboard():
    total_negocios = Negocio.query.count()
    pendientes = Negocio.query.filter_by(estado="pendiente").count()
    aprobados = Negocio.query.filter_by(estado="aprobado").count()
    usuarios = Usuario.query.count()
    categorias = Categoria.query.count()
    noticias = Noticia.query.count()
    return render_template(
        "admin/dashboard.html",
        total_negocios=total_negocios,
        pendientes=pendientes,
        aprobados=aprobados,
        usuarios=usuarios,
        categorias=categorias,
        noticias=noticias,
    )

# ---------- Negocios ----------
@admin_bp.route("/negocios", methods=["GET"])
@login_required
@admin_required
def admin_negocios():
    estado = request.args.get("estado")
    query = Negocio.query
    if estado:
        query = query.filter_by(estado=estado)
    negocios = query.order_by(Negocio.id.desc()).all()
    return render_template("admin/negocios.html", negocios=negocios, estado=estado)

@admin_bp.route("/negocios/<int:id>/aprobar", methods=["POST"])
@login_required
@admin_required
def aprobar_negocio(id):
    negocio = Negocio.query.get_or_404(id)
    negocio.estado = "aprobado"
    db.session.commit()
    flash(f"✅ Negocio '{negocio.nombre}' aprobado.", "success")
    return redirect(url_for("admin.admin_negocios"))

@admin_bp.route("/negocios/<int:id>/rechazar", methods=["POST"])
@login_required
@admin_required
def rechazar_negocio(id):
    negocio = Negocio.query.get_or_404(id)
    negocio.estado = "rechazado"
    db.session.commit()
    flash(f"🚫 Negocio '{negocio.nombre}' rechazado.", "danger")
    return redirect(url_for("admin.admin_negocios"))


@admin_bp.route("/negocios/<int:id>/eliminar", methods=["POST"])
@login_required
@admin_required
def eliminar_negocio(id):
    """Permite a un administrador eliminar un negocio."""
    negocio = Negocio.query.get_or_404(id)
    nombre = negocio.nombre
    db.session.delete(negocio)
    db.session.commit()
    flash(f"🗑️ El negocio '{nombre}' fue eliminado correctamente.", "success")
    return redirect(url_for("admin.admin_negocios"))


# ---------- Avisos ----------
@admin_bp.route("/avisos", methods=["GET"])
@login_required
@admin_required
def admin_avisos():
    avisos = Aviso.query.order_by(Aviso.fecha_inicio.desc()).all()
    return render_template("admin/avisos.html", avisos=avisos)

@admin_bp.route("/avisos/crear", methods=["GET", "POST"])
@login_required
@admin_required
def crear_aviso():
    if request.method == "POST":
        mensaje = request.form.get("mensaje", "").strip()
        fecha_inicio = request.form.get("fecha_inicio", "").strip()
        fecha_fin = request.form.get("fecha_fin", "").strip()
        if not mensaje or not fecha_inicio:
            flash("⚠️ Debes ingresar al menos un mensaje y fecha de inicio.", "warning")
            return redirect(url_for("admin.crear_aviso"))
        try:
            f_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            f_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date() if fecha_fin else None
            if f_fin and f_fin < f_inicio:
                flash("La fecha de fin no puede ser anterior al inicio.", "warning")
                return redirect(url_for("admin.crear_aviso"))
        except ValueError:
            flash("Formato de fecha inválido.", "danger")
            return redirect(url_for("admin.crear_aviso"))
        aviso = Aviso(mensaje=mensaje, fecha_inicio=f_inicio, fecha_fin=f_fin)
        db.session.add(aviso)
        db.session.commit()
        flash("✅ Aviso creado con éxito.", "success")
        return redirect(url_for("admin.admin_avisos"))
    return render_template("admin/crear_aviso.html")

@admin_bp.route("/avisos/<int:id>/eliminar", methods=["POST"])
@login_required
@admin_required
def eliminar_aviso(id):
    aviso = Aviso.query.get_or_404(id)
    db.session.delete(aviso)
    db.session.commit()
    flash("🗑️ Aviso eliminado correctamente.", "success")
    return redirect(url_for("admin.admin_avisos"))

# ---------- Noticias ----------
@admin_bp.route("/noticias", methods=["GET"])
@login_required
@admin_required
def admin_noticias():
    noticias = Noticia.query.order_by(Noticia.fecha.desc()).all()
    return render_template("admin/noticias.html", noticias=noticias)

@admin_bp.route("/noticias/crear", methods=["GET", "POST"])
@login_required
@admin_required
def crear_noticia():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        contenido = request.form.get("contenido", "").strip()
        if not titulo or not contenido:
            flash("⚠️ Título y contenido son obligatorios.", "warning")
            return redirect(url_for("admin.crear_noticia"))
        fecha = datetime.now().date()
        imagen_file = request.files.get("imagen")
        imagen_rel = save_image(imagen_file) if imagen_file else None
        noticia = Noticia(titulo=titulo, contenido=contenido, fecha=fecha, imagen=imagen_rel)
        db.session.add(noticia)
        db.session.commit()
        flash("📰 Noticia publicada con éxito.", "success")
        return redirect(url_for("admin.admin_noticias"))
    return render_template("admin/crear_noticia.html")

@admin_bp.route("/noticias/<int:id>/eliminar", methods=["POST"])
@login_required
@admin_required
def eliminar_noticia(id):
    noticia = Noticia.query.get_or_404(id)
    db.session.delete(noticia)
    db.session.commit()
    flash("🗑️ Noticia eliminada correctamente.", "success")
    return redirect(url_for("admin.admin_noticias"))

# ---------- Eventos ----------
@admin_bp.route("/eventos", methods=["GET"])
@login_required
@admin_required
def admin_eventos():
    eventos = Evento.query.order_by(Evento.fecha.desc()).all()
    return render_template("admin/eventos.html", eventos=eventos)

@admin_bp.route("/eventos/crear", methods=["GET", "POST"])
@login_required
@admin_required
def crear_evento():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        lugar = request.form.get("lugar", "").strip()
        fecha = request.form.get("fecha", "").strip()
        imagen_file = request.files.get("imagen")

        if not titulo or not descripcion or not lugar or not fecha:
            flash("⚠️ Todos los campos son obligatorios.", "warning")
            return redirect(url_for("admin.crear_evento"))

        try:
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            flash("Formato de fecha inválido.", "danger")
            return redirect(url_for("admin.crear_evento"))

        imagen_rel = save_image(imagen_file) if imagen_file else None

        evento = Evento(
            titulo=titulo,
            descripcion=descripcion,
            lugar=lugar,
            fecha=fecha_dt,
            imagen=imagen_rel
        )
        db.session.add(evento)
        db.session.commit()
        flash("🎉 Evento creado correctamente.", "success")
        return redirect(url_for("admin.admin_eventos"))

    return render_template("admin/crear_evento.html")


@admin_bp.route("/eventos/<int:id>/eliminar", methods=["POST"])
@login_required
@admin_required
def eliminar_evento(id):
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    flash("🗑️ Evento eliminado correctamente.", "success")
    return redirect(url_for("admin.admin_eventos"))
