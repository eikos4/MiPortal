from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, uuid

from . import ciudadano_bp
from .models import PerfilEmpresa, Evento, Aviso, NoticiaEmpresa, Oferta
from .forms import OfertaForm, PerfilEmpresaForm
from mi_comuna.modules.inicio.forms import AvisoForm
from mi_comuna.extensions import db


# --------------------------
# Helper: guardar imagen
# --------------------------
def save_image(file_storage):
    if not file_storage or file_storage.filename == "":
        return None

    allowed = {"png", "jpg", "jpeg", "webp", "gif"}
    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    if ext not in allowed:
        raise ValueError("Formato de imagen no permitido")

    filename = secure_filename(file_storage.filename)
    unique = f"{uuid.uuid4().hex}_{filename}"

    upload_root = current_app.config.get("UPLOAD_FOLDER") or os.path.join("mi_comuna", "static", "uploads")
    os.makedirs(upload_root, exist_ok=True)

    path = os.path.join(upload_root, unique)
    file_storage.save(path)

    return f"uploads/{unique}"  # ruta relativa para servir desde /static


# --------------------------
# Dashboard
# --------------------------
@ciudadano_bp.route("/dashboard", endpoint="dashboard")
@login_required
def dashboard():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
    return render_template("ciudadano/dashboard.html", perfil=perfil)


# --------------------------
# Perfil Empresa
# --------------------------
@ciudadano_bp.route("/perfil", methods=["GET", "POST"], endpoint="perfil")
@login_required
def perfil():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()

    form = PerfilEmpresaForm(obj=perfil)  # carga datos existentes en el form

    if form.validate_on_submit():
        if not perfil:
            perfil = PerfilEmpresa(usuario_id=current_user.id)

        perfil.nombre = form.nombre.data
        perfil.descripcion = form.descripcion.data
        perfil.direccion = form.direccion.data
        perfil.telefono = form.telefono.data
        perfil.redes = form.redes.data

        db.session.add(perfil)
        db.session.commit()
        flash("✅ Perfil actualizado correctamente", "success")
        return redirect(url_for("ciudadano.perfil"))

    return render_template("ciudadano/perfil.html", perfil=perfil, form=form)


# --------------------------
# Ofertas
# --------------------------
@ciudadano_bp.route("/ofertas", methods=["GET", "POST"], endpoint="ofertas")
@login_required
def ofertas():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
    if not perfil:
        flash("⚠️ Debes crear tu perfil de empresa antes de publicar ofertas.", "warning")
        return redirect(url_for("ciudadano.perfil"))

    form = OfertaForm()
    if form.validate_on_submit():
        try:
            imagen_rel = save_image(form.imagen.data) if form.imagen.data else None
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("ciudadano/ofertas.html", form=form, ofertas=perfil.ofertas, perfil=perfil)

        nueva = Oferta(
            titulo=form.titulo.data.strip(),
            descripcion=form.descripcion.data.strip(),
            empresa_id=perfil.id,
            imagen=imagen_rel
        )
        db.session.add(nueva)
        db.session.commit()
        flash("✅ Oferta publicada correctamente", "success")
        return redirect(url_for("ciudadano.ofertas"))

    ofertas = Oferta.query.filter_by(empresa_id=perfil.id).order_by(Oferta.fecha_inicio.desc().nullslast()).all()
    return render_template("ciudadano/ofertas.html", form=form, ofertas=ofertas, perfil=perfil)


# --------------------------
# Avisos
# --------------------------
@ciudadano_bp.route("/avisos", methods=["GET", "POST"], endpoint="avisos")
@login_required
def avisos():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first_or_404()
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
            empresa_id=perfil.id
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Aviso publicado correctamente", "success")
        return redirect(url_for("ciudadano.avisos"))

    return render_template("ciudadano/avisos.html", form=form, avisos=perfil.avisos, perfil=perfil)


# --------------------------
from .forms import NoticiaForm, EventoForm

# Noticias
@ciudadano_bp.route("/noticias", methods=["GET", "POST"], endpoint="noticias")
@login_required
def noticias():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first_or_404()
    form = NoticiaForm()
    if form.validate_on_submit():
        nueva = NoticiaEmpresa(
            titulo=form.titulo.data,
            contenido=form.contenido.data,
            imagen=form.imagen.data.filename if form.imagen.data else None,
            empresa_id=perfil.id
        )
        db.session.add(nueva)
        db.session.commit()
        flash("✅ Noticia publicada correctamente", "success")
        return redirect(url_for("ciudadano.noticias"))
    return render_template("ciudadano/noticias.html", form=form, noticias=perfil.noticias)

# Eventos
@ciudadano_bp.route("/eventos", methods=["GET", "POST"], endpoint="eventos")
@login_required
def eventos():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first_or_404()
    form = EventoForm()
    if form.validate_on_submit():
        nuevo = Evento(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            fecha=form.fecha.data,
            lugar=form.lugar.data,
            imagen=form.imagen.data.filename if form.imagen.data else None,
            empresa_id=perfil.id
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Evento publicado correctamente", "success")
        return redirect(url_for("ciudadano.eventos"))
    return render_template("ciudadano/eventos.html", form=form, eventos=perfil.eventos)
