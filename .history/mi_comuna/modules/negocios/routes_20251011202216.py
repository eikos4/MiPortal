# mi_comuna/modules/negocios/routes.py
import os, re, uuid
from datetime import date
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from mi_comuna.extensions import db
from . import negocios_bp
from .models import Negocio, Categoria
from mi_comuna.modules.ciudadano.models import PerfilEmpresa, EventoCiudadano, AvisoCiudadano, NoticiaEmpresa, OfertaCiudadano


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


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
    return f"uploads/{unique}"


# ---------- Listado principal ----------
@negocios_bp.route("/", methods=["GET"], endpoint="lista_negocios")
def lista_negocios():
    q = request.args.get("q", "", type=str).strip()
    categoria_id = request.args.get("categoria", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 9, type=int), 30)

    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    query = Negocio.query.options(joinedload(Negocio.categoria)).filter_by(estado="aprobado")

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Negocio.nombre.ilike(like),
                Negocio.descripcion.ilike(like),
                Negocio.direccion.ilike(like),
            )
        )
    if categoria_id:
        query = query.filter(Negocio.categoria_id == categoria_id)

    if q or categoria_id:
        pag = query.order_by(Negocio.nombre.asc()).paginate(page=page, per_page=per_page, error_out=False)
        return render_template(
            "negocios/lista.html",
            categorias=categorias,
            negocios=pag.items,
            pag=pag,
            q=q,
            categoria_actual=categoria_id,
            top_por_categoria=None,
        )

    top_por_categoria = []
    for cat in categorias:
        top = (
            Negocio.query.options(joinedload(Negocio.categoria))
            .filter_by(categoria_id=cat.id, estado="aprobado")
            .order_by(Negocio.id.desc())
            .limit(3)
            .all()
        )
        if top:
            top_por_categoria.append({"categoria": cat, "slug": slugify(cat.nombre), "negocios": top})

    return render_template(
        "negocios/lista.html",
        categorias=categorias,
        top_por_categoria=top_por_categoria,
        negocios=None,
        pag=None,
        q="",
        categoria_actual=None,
    )


# ---------- Por categoría con slug ----------
@negocios_bp.route("/categoria/<int:cat_id>-<slug>", methods=["GET"], endpoint="por_categoria")
def por_categoria(cat_id, slug):
    cat = Categoria.query.get_or_404(cat_id)
    expected_slug = slugify(cat.nombre)
    if slug != expected_slug:
        return redirect(url_for("negocios.por_categoria", cat_id=cat.id, slug=expected_slug), code=301)

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 12, type=int), 30)

    query = (
        Negocio.query.options(joinedload(Negocio.categoria))
        .filter_by(categoria_id=cat.id, estado="aprobado")
        .order_by(Negocio.nombre.asc())
    )
    pag = query.paginate(page=page, per_page=per_page, error_out=False)

    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    return render_template("negocios/por_categoria.html", categoria=cat, categorias=categorias, negocios=pag.items, pag=pag)


# ---------- Detalle ----------
@negocios_bp.route("/<int:id>", methods=["GET"], endpoint="detalle")
def detalle(id):
    negocio = Negocio.query.get_or_404(id)

    perfil = negocio.usuario.perfil if (negocio.usuario and hasattr(negocio.usuario, "perfil")) else None

    feed = []

    if perfil:
        # Avisos
        for a in perfil.avisos.order_by(AvisoCiudadano.creado_en.desc()).all():
            fecha_ref = a.creado_en.date() if a.creado_en else date.today()
            feed.append(
                {
                    "tipo": "aviso",
                    "fecha": fecha_ref,
                    "titulo": a.titulo or "Aviso",
                    "descripcion": a.descripcion or "",
                    "imagen": a.imagen,
                    "extra": {"inicio": None, "fin": None},
                }
            )

        # Eventos
        for e in perfil.eventos.order_by(EventoCiudadano.creado_en.desc()).all():
            feed.append(
                {
                    "tipo": "evento",
                    "fecha": e.fecha_inicio or date.today(),
                    "titulo": e.titulo,
                    "descripcion": e.descripcion or "",
                    "imagen": e.imagen,
                    "extra": {"fecha": e.fecha_inicio, "lugar": e.lugar},
                }
            )

        # Noticias
        for n in perfil.noticias.order_by(NoticiaEmpresa.fecha_publicacion.desc()).all():
            feed.append(
                {
                    "tipo": "noticia",
                    "fecha": n.fecha_publicacion.date() if n.fecha_publicacion else date.today(),
                    "titulo": n.titulo,
                    "descripcion": n.contenido or "",
                    "imagen": n.imagen,
                    "extra": {"fecha": n.fecha_publicacion},
                }
            )

        # Ofertas
        for o in perfil.ofertas.order_by(OfertaCiudadano.creado_en.desc()).all():
            feed.append(
                {
                    "tipo": "oferta",
                    "fecha": o.fecha_inicio or date.today(),
                    "titulo": o.titulo or "Oferta",
                    "descripcion": o.descripcion or "",
                    "imagen": o.imagen,
                    "extra": {
                        "inicio": o.fecha_inicio,
                        "fin": o.fecha_fin,
                        "vigente": o.vigente,  # propiedad bool
                    },
                }
            )

    # Ordenar por fecha desc
    feed.sort(key=lambda x: x["fecha"] or date.today(), reverse=True)

    return render_template("negocios/detalle.html", negocio=negocio, perfil=perfil, feed=feed)


# ---------- Registrar ----------
@negocios_bp.route("/registrar", methods=["GET", "POST"], endpoint="registrar")
@login_required
def registrar():
    from .forms import NegocioForm

    if Negocio.query.filter_by(usuario_id=current_user.id).first():
        flash("⚠️ Solo puedes registrar un negocio. Adminístralo desde tu perfil.", "warning")
        return redirect(url_for("ciudadano.dashboard"))

    form = NegocioForm()
    categorias_db = Categoria.query.order_by(Categoria.nombre.asc()).all()
    form.categoria_id.choices = [(c.id, c.nombre) for c in categorias_db]

    if form.validate_on_submit():
        try:
            imagen_rel = save_image(form.imagen.data) if form.imagen.data else None
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("negocios/register.html", form=form, categorias=categorias_db)

        perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
        if not perfil:
            perfil = PerfilEmpresa(
                usuario_id=current_user.id,
                nombre=form.nombre.data.strip(),
                descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
                direccion=form.direccion.data.strip(),
            )
            db.session.add(perfil)
            db.session.commit()

        nuevo = Negocio(
            nombre=form.nombre.data.strip(),
            descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
            direccion=form.direccion.data.strip(),
            telefono=form.telefono.data.strip() if form.telefono.data else None,
            whatsapp=form.whatsapp.data.strip() if form.whatsapp.data else None,
            redes=form.redes.data.strip() if form.redes.data else None,
            horario=form.horario.data.strip() if hasattr(form, "horario") and form.horario.data else None,
            categoria_id=form.categoria_id.data,
            usuario_id=current_user.id,
            estado="pendiente",
            imagen=imagen_rel,
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Tu negocio fue registrado y está pendiente de aprobación.", "success")
        return redirect(url_for("ciudadano.dashboard"))

    return render_template("negocios/register.html", form=form, categorias=categorias_db)
