import os, uuid
from flask import abort, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import ciudadano_bp
from .models import PerfilEmpresa, Evento, Aviso, NoticiaEmpresa, Oferta
from .forms import OfertaForm, PerfilEmpresaForm, AvisoForm, NoticiaForm, EventoForm
from mi_comuna.modules.negocios.models import Categoria
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
    form = PerfilEmpresaForm(obj=perfil)

    # cargar categorías
    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    form.categoria_id.choices = [(c.id, c.nombre) for c in categorias]

    if form.validate_on_submit():
        if not perfil:
            perfil = PerfilEmpresa(usuario_id=current_user.id)

        perfil.nombre = form.nombre.data.strip()
        perfil.descripcion = form.descripcion.data.strip() if form.descripcion.data else None
        perfil.direccion = form.direccion.data.strip() if form.direccion.data else None
        perfil.telefono = form.telefono.data.strip() if form.telefono.data else None
        perfil.whatsapp = form.whatsapp.data.strip() if form.whatsapp.data else None
        perfil.email = form.email.data.strip() if form.email.data else None
        perfil.sitio_web = form.sitio_web.data.strip() if form.sitio_web.data else None
        perfil.facebook = form.facebook.data.strip() if form.facebook.data else None
        perfil.instagram = form.instagram.data.strip() if form.instagram.data else None
        perfil.tiktok = form.tiktok.data.strip() if form.tiktok.data else None
        perfil.horario = form.horario.data.strip() if form.horario.data else None
        perfil.categoria_id = form.categoria_id.data

        # logo opcional
        if form.logo.data:
            try:
                perfil.logo = save_image(form.logo.data)
            except ValueError as e:
                flash(str(e), "danger")

        db.session.add(perfil)
        db.session.commit()
        flash("✅ Perfil actualizado correctamente", "success")
        return redirect(url_for("ciudadano.perfil"))

    return render_template("ciudadano/perfil.html", form=form, perfil=perfil)


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
            perfil_id=perfil.id,  # ✅ corregido
            imagen=imagen_rel,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data
        )
        db.session.add(nueva)
        db.session.commit()
        flash("✅ Oferta publicada correctamente", "success")
        return redirect(url_for("ciudadano.ofertas"))

    ofertas = Oferta.query.filter_by(perfil_id=perfil.id).order_by(Oferta.creado_en.desc()).all()
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
            perfil_id=perfil.id  # ✅ corregido
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Aviso publicado correctamente", "success")
        return redirect(url_for("ciudadano.avisos"))

    return render_template("ciudadano/avisos.html", form=form, avisos=perfil.avisos, perfil=perfil)


# --------------------------
# Noticias
# --------------------------
@ciudadano_bp.route("/noticias", methods=["GET", "POST"], endpoint="noticias")
@login_required
def noticias():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first_or_404()
    form = NoticiaForm()

    if form.validate_on_submit():
        try:
            imagen_rel = save_image(form.imagen.data) if form.imagen.data else None
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("ciudadano/noticias.html", form=form, noticias=perfil.noticias, perfil=perfil)

        nueva = NoticiaEmpresa(
            titulo=form.titulo.data.strip(),
            contenido=form.contenido.data.strip(),
            imagen=imagen_rel,
            perfil_id=perfil.id  # ✅ corregido
        )
        db.session.add(nueva)
        db.session.commit()
        flash("✅ Noticia publicada correctamente", "success")
        return redirect(url_for("ciudadano.noticias"))

    return render_template("ciudadano/noticias.html", form=form, noticias=perfil.noticias, perfil=perfil)


# --------------------------
# Eventos
# --------------------------
@ciudadano_bp.route("/eventos", methods=["GET", "POST"], endpoint="eventos")
@login_required
def eventos():
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first_or_404()
    form = EventoForm()

    if form.validate_on_submit():
        try:
            imagen_rel = save_image(form.imagen.data) if form.imagen.data else None
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("ciudadano/eventos.html", form=form, eventos=perfil.eventos, perfil=perfil)

        nuevo = Evento(
            titulo=form.titulo.data.strip(),
            descripcion=form.descripcion.data.strip(),
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            lugar=form.lugar.data.strip() if form.lugar.data else None,
            imagen=imagen_rel,
            perfil_id=perfil.id  # ✅ corregido
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Evento publicado correctamente", "success")
        return redirect(url_for("ciudadano.eventos"))

    return render_template("ciudadano/eventos.html", form=form, eventos=perfil.eventos, perfil=perfil)


@ciudadano_bp.route("/eventos/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_evento(id):
    evento = Evento.query.get_or_404(id)

    # Validar que el evento pertenece al usuario actual
    if not evento.empresa or evento.empresa.usuario_id != current_user.id:
        abort(403)

    db.session.delete(evento)
    db.session.commit()
    flash("✅ Evento eliminado correctamente", "success")
    return redirect(url_for("ciudadano.eventos"))
