import os, uuid
from flask import abort, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from mi_comuna.modules.ciudadano.decorators import ciudadano_required
from mi_comuna.extensions import db
from mi_comuna.modules.negocios.models import Categoria
from mi_comuna.modules.aviso.models import Aviso

from . import ciudadano_bp
from .models import PerfilEmpresa, Evento, NoticiaEmpresa, Oferta
from .forms import PerfilEmpresaForm, AvisoForm, EventoForm, NoticiaForm, OfertaForm


# ======================================================
# 🧩 Helper para guardar imágenes de forma segura
# ======================================================
def save_image(file_storage):
    """Guarda una imagen en la carpeta /static/uploads y retorna su ruta relativa."""
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

    file_path = os.path.join(upload_root, unique_name)
    file_storage.save(file_path)

    return f"uploads/{unique_name}"  # Ruta relativa (usable desde /static/uploads/...)


# ======================================================
# 🏠 Dashboard Principal
# ======================================================
@ciudadano_bp.route("/dashboard")
@login_required
def dashboard():
    """Panel principal del ciudadano."""
    if current_user.rol == "admin":
        return redirect(url_for("admin.dashboard"))

    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()

    # Si no tiene perfil, redirigir a crearlo
    if current_user.rol == "ciudadano" and not perfil:
        return redirect(url_for("ciudadano.perfil"))

    return render_template("ciudadano/dashboard.html", perfil=perfil)


# ======================================================
# 🏢 Perfil de Empresa
# ======================================================
@ciudadano_bp.route("/perfil", methods=["GET", "POST"], endpoint="perfil")
@login_required
@ciudadano_required
def perfil():
    """Creación o edición del perfil de empresa."""
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
    form = PerfilEmpresaForm(obj=perfil)

    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    form.categoria_id.choices = [(c.id, c.nombre) for c in categorias]

    if form.validate_on_submit():
        if not perfil:
            perfil = PerfilEmpresa(usuario_id=current_user.id)

        # Campos básicos
        for field in [
            "nombre", "descripcion", "direccion", "telefono", "whatsapp", "email",
            "sitio_web", "facebook", "instagram", "tiktok", "horario"
        ]:
            setattr(perfil, field, getattr(form, field).data.strip() if getattr(form, field).data else None)

        perfil.categoria_id = form.categoria_id.data

        # Guardar logo (opcional)
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
# 💰 Ofertas
# ======================================================
@ciudadano_bp.route("/ofertas", methods=["GET", "POST"], endpoint="ofertas")
@login_required
@ciudadano_required
def ofertas():
    """Publicación y listado de ofertas."""
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
            perfil_id=perfil.id,
            imagen=imagen_rel,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
        )
        db.session.add(nueva)
        db.session.commit()
        flash("✅ Oferta publicada correctamente.", "success")
        return redirect(url_for("ciudadano.ofertas"))

    ofertas = Oferta.query.filter_by(perfil_id=perfil.id).order_by(Oferta.creado_en.desc()).all()
    return render_template("ciudadano/ofertas.html", form=form, ofertas=ofertas, perfil=perfil)


# ======================================================
# 📢 Avisos
# ======================================================
@ciudadano_bp.route("/avisos", methods=["GET", "POST"], endpoint="avisos")
@login_required
@ciudadano_required
def avisos():
    """Gestión de avisos por el ciudadano."""
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


# ======================================================
# 🗑️ Eliminar Aviso
# ======================================================
@ciudadano_bp.route("/avisos/<int:id>/eliminar", methods=["POST"], endpoint="eliminar_aviso")
@login_required
@ciudadano_required
def eliminar_aviso(id):
    """Elimina un aviso del perfil del ciudadano."""
    aviso = Aviso.query.get_or_404(id)

    if not aviso.perfil or aviso.perfil.usuario_id != current_user.id:
        abort(403)

    db.session.delete(aviso)
    db.session.commit()
    flash("🗑 Aviso eliminado correctamente.", "success")
    return redirect(url_for("ciudadano.avisos"))


# ======================================================
# 📰 Noticias
# ======================================================
@ciudadano_bp.route("/noticias", methods=["GET", "POST"], endpoint="noticias")
@login_required
@ciudadano_required
def noticias():
    """Publicación y listado de noticias."""
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
    if not perfil:
        flash("⚠️ Debes crear tu perfil antes de publicar noticias.", "warning")
        return redirect(url_for("ciudadano.perfil"))

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
            perfil_id=perfil.id,
        )
        db.session.add(nueva)
        db.session.commit()
        flash("✅ Noticia publicada correctamente.", "success")
        return redirect(url_for("ciudadano.noticias"))

    noticias = NoticiaEmpresa.query.filter_by(perfil_id=perfil.id).order_by(NoticiaEmpresa.creado_en.desc()).all()
    return render_template("ciudadano/noticias.html", form=form, noticias=noticias, perfil=perfil)


# ======================================================
# 🎉 Eventos
# ======================================================
@ciudadano_bp.route("/eventos", methods=["GET", "POST"], endpoint="eventos")
@login_required
@ciudadano_required
def eventos():
    """Gestión de eventos del ciudadano."""
    perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
    if not perfil:
        flash("⚠️ Debes crear tu perfil antes de publicar eventos.", "warning")
        return redirect(url_for("ciudadano.perfil"))

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
            perfil_id=perfil.id,
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Evento publicado correctamente.", "success")
        return redirect(url_for("ciudadano.eventos"))

    eventos = Evento.query.filter_by(perfil_id=perfil.id).order_by(Evento.creado_en.desc()).all()
    return render_template("ciudadano/eventos.html", form=form, eventos=eventos, perfil=perfil)


# ======================================================
# 🗑️ Eliminaciones seguras (Eventos / Noticias / Ofertas)
# ======================================================
@ciudadano_bp.route("/eventos/<int:id>/eliminar", methods=["POST"], endpoint="eliminar_evento")
@login_required
@ciudadano_required
def eliminar_evento(id):
    evento = Evento.query.get_or_404(id)
    if not evento.perfil or evento.perfil.usuario_id != current_user.id:
        abort(403)
    db.session.delete(evento)
    db.session.commit()
    flash("✅ Evento eliminado correctamente.", "success")
    return redirect(url_for("ciudadano.eventos"))


@ciudadano_bp.route("/noticias/<int:id>/eliminar", methods=["POST"], endpoint="eliminar_noticia")
@login_required
@ciudadano_required
def eliminar_noticia(id):
    noticia = NoticiaEmpresa.query.get_or_404(id)
    if not noticia.perfil or noticia.perfil.usuario_id != current_user.id:
        abort(403)
    db.session.delete(noticia)
    db.session.commit()
    flash("✅ Noticia eliminada correctamente.", "success")
    return redirect(url_for("ciudadano.noticias"))


@ciudadano_bp.route("/ofertas/<int:id>/eliminar", methods=["POST"], endpoint="eliminar_oferta")
@login_required
@ciudadano_required
def eliminar_oferta(id):
    oferta = Oferta.query.get_or_404(id)
    if not oferta.perfil or oferta.perfil.usuario_id != current_user.id:
        abort(403)
    db.session.delete(oferta)
    db.session.commit()
    flash("✅ Oferta eliminada correctamente.", "success")
    return redirect(url_for("ciudadano.ofertas"))
