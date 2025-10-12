# mi_comuna/modules/negocios/routes.py
import os, re, uuid
from datetime import date, datetime
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
# ---------- Detalle de negocio ----------
from datetime import datetime, date

@negocios_bp.route("/<int:id>", methods=["GET"], endpoint="detalle")
def detalle(id):
    negocio = Negocio.query.get_or_404(id)

    # 🔹 Buscar el perfil asociado al negocio
    perfil = None
    if negocio.usuario_id:
        perfil = PerfilEmpresa.query.filter_by(usuario_id=negocio.usuario_id).first()

    if not perfil:
        return render_template("negocios/detalle.html", negocio=negocio, perfil=None, feed=[])

    feed = []

    # --- 📢 Avisos ---
    for a in getattr(perfil, "avisos", []):
        feed.append({
            "tipo": "aviso",
            "fecha": getattr(a, "creado_en", None),
            "titulo": a.titulo or "Aviso",
            "descripcion": a.descripcion or "",
            "imagen": a.imagen,
            "extra": {
                "inicio": getattr(a, "fecha_inicio", None),
                "fin": getattr(a, "fecha_fin", None)
            }
        })

    # --- 🎉 Eventos ---
    for e in getattr(perfil, "eventos", []):
        feed.append({
            "tipo": "evento",
            "fecha": getattr(e, "fecha_inicio", None),
            "titulo": e.titulo or "Evento",
            "descripcion": e.descripcion or "",
            "imagen": e.imagen,
            "extra": {
                "fecha": getattr(e, "fecha_inicio", None),
                "lugar": getattr(e, "lugar", None)
            }
        })

    # --- 📰 Noticias ---
    for n in getattr(perfil, "noticias", []):
        feed.append({
            "tipo": "noticia",
            "fecha": getattr(n, "fecha_publicacion", None),
            "titulo": n.titulo or "Noticia",
            "descripcion": n.contenido or "",
            "imagen": n.imagen,
            "extra": {
                "fecha": getattr(n, "fecha_publicacion", None)
            }
        })

    # --- 💸 Ofertas ---
    for o in getattr(perfil, "ofertas", []):
        vigente_flag = None
        try:
            vigente_flag = o.vigente() if callable(o.vigente) else bool(o.vigente)
        except Exception:
            vigente_flag = None

        feed.append({
            "tipo": "oferta",
            "fecha": getattr(o, "fecha_inicio", None),
            "titulo": o.titulo or "Oferta",
            "descripcion": o.descripcion or "",
            "imagen": o.imagen,
            "extra": {
                "inicio": getattr(o, "fecha_inicio", None),
                "fin": getattr(o, "fecha_fin", None),
                "vigente": vigente_flag
            }
        })

    # --- 🧩 Normalizar TODAS las fechas a datetime ---
    def normalize_fecha(value):
        """Convierte cualquier tipo de fecha en datetime seguro."""
        if not value:
            return datetime.utcnow()
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        return datetime.utcnow()

    for item in feed:
        item["fecha"] = normalize_fecha(item.get("fecha"))

    # --- 🔹 Ordenar por fecha descendente (más recientes primero)
    feed.sort(key=lambda x: x["fecha"], reverse=True)

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
