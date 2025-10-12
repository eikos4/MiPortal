from flask import render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, uuid

from mi_comuna.extensions import db
from mi_comuna.modules.negocios.models import Categoria
from mi_comuna.modules.ciudadano.decorators import ciudadano_required

from . import ciudadano_bp
from .models import (
    PerfilEmpresa,
    AvisoCiudadano as Aviso,
    EventoCiudadano as Evento,
    NoticiaEmpresa,
    OfertaCiudadano as Oferta
)
from .forms import PerfilEmpresaForm, AvisoForm, EventoForm, NoticiaForm, OfertaForm


# ======================================================
# 🧩 Guardar imagen
# ======================================================
def save_image(file_storage):
    if not file_storage or file_storage.filename == "":
        return None

    allowed = {"png", "jpg", "jpeg", "webp", "gif"}
    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    if ext not in allowed:
        raise ValueError("Formato de imagen no permitido")

    filename = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"

    upload_root = current_app.config.get("UPLOAD_FOLDER") or os.path.join("mi_comuna", "static", "uploads")
    os.makedirs(upload_root, exist_ok=True)
    file_storage.save(os.path.join(upload_root, unique_name))
    return f"uploads/{unique_name}"


# ======================================================
# 🏠 Dashboard
# ======================================================
@ciudadano_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.rol == "admin":
        return redirect(url_for("admin.dashboard"))

    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
    if current_user.rol == "ciudadano" and not perfil:
        return redirect(url_for("ciudadano.perfil"))

    return render_template("ciudadano/dashboard.html", perfil=perfil)


# ======================================================
# 🏢 Perfil
# ======================================================
@ciudadano_bp.route("/perfil", methods=["GET", "POST"])
@login_required
@ciudadano_required
def perfil():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
    form = PerfilEmpresaForm(obj=perfil)
    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    form.categoria_id.choices = [(c.id, c.nombre) for c in categorias]

    if form.validate_on_submit():
        if not perfil:
            perfil = PerfilEmpresa(usuario_id=current_user.id)

        for field in [
            "nombre", "descripcion", "direccion", "telefono", "whatsapp", "email",
            "sitio_web", "facebook", "instagram", "tiktok", "horario"
        ]:
            setattr(perfil, field, getattr(form, field).data.strip() if getattr(form, field).data else None)

        perfil.categoria_id = form.categoria_id.data
        if form.logo.data:
            try:
                perfil.logo = save_image(form.logo.data)
            except ValueError as e:
                flash(str(e), "danger")

        db.session.add(perfil)
        db.session.commit()
        flash("✅ Perfil actualizado correctamente.", "success")
        return redirect(url_for("ciudadano.perfil"))

    return render_template("ciudadano/perfil.html", form=form, perfil=perfil)


# ======================================================
# 📢 Avisos
# ======================================================
@ciudadano_bp.route("/avisos", methods=["GET", "POST"])
@login_required
@ciudadano_required
def avisos():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
    if not perfil:
        flash("⚠️ Debes crear tu perfil antes de publicar avisos.", "warning")
        return redirect(url_for("ciudadano.perfil"))

    form = AvisoForm()
    if form.validate_on_submit():
        try:
            imagen_rel = save_image(form.imagen.data) if form.imagen.data else None
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("ciudadano/avisos.html", form=form, avisos=perfil.avisos, perfil=perfil)

        nuevo = Aviso(
            titulo=form.titulo.data.strip(),
            descripcion=form.descripcion.data.strip(),
            imagen=imagen_rel,
            perfil_id=perfil.id,
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Aviso publicado correctamente.", "success")
        return redirect(url_for("ciudadano.avisos"))

    avisos = Aviso.query.filter_by(perfil_id=perfil.id).order_by(Aviso.creado_en.desc()).all()
    return render_template("ciudadano/avisos.html", form=form, avisos=avisos, perfil=perfil)


@ciudadano_bp.route("/avisos/<int:id>/eliminar", methods=["POST"])
@login_required
@ciudadano_required
def eliminar_aviso(id):
    aviso = Aviso.query.get_or_404(id)
    if not aviso.perfil or aviso.perfil.usuario_id != current_user.id:
        abort(403)
    db.session.delete(aviso)
    db.session.commit()
    flash("🗑 Aviso eliminado correctamente.", "success")
    return redirect(url_for("ciudadano.avisos"))
