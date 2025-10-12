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
from .forms import NegocioForm
from mi_comuna.modules.ciudadano.models import PerfilEmpresa


# ----------------------------------------------------
# 🔹 Helpers
# ----------------------------------------------------
def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    return re.sub(r"[-\s]+", "-", text)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "webp", "gif"}

def save_image(file_storage):
    """Guarda una imagen en /static/uploads y retorna la ruta relativa."""
    if not file_storage or file_storage.filename == "":
        return None

    allowed = {"png", "jpg", "jpeg", "webp", "gif"}
    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    if ext not in allowed:
        raise ValueError("Formato de imagen no permitido")

    filename = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"

    upload_folder = current_app.config.get("UPLOAD_FOLDER") or os.path.join("mi_comuna", "static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    path = os.path.join(upload_folder, unique_name)
    file_storage.save(path)

    return f"uploads/{unique_name}"


# ----------------------------------------------------
# 🔹 Listado principal
# ----------------------------------------------------
@negocios_bp.route("/", methods=["GET"], endpoint="lista_negocios")
@negocios_bp.route("/", endpoint="lista")
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
            or_(Negocio.nombre.ilike(like),
                Negocio.descripcion.ilike(like),
                Negocio.direccion.ilike(like))
        )
    if categoria_id:
        query = query.filter(Negocio.categoria_id == categoria_id)

    # Filtro activo o búsqueda
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

    # Top por categoría
    top_por_categoria = []
    for cat in categorias:
        top = (
            Negocio.query.options(joinedload(Negocio.categoria))
            .filter_by(categoria_id=cat.id, estado="aprobado")
            .order_by(Negocio.id.desc()).limit(3).all()
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


# ----------------------------------------------------
# 🔹 Por categoría con slug
# ----------------------------------------------------
@negocios_bp.route("/categoria/<int:cat_id>-<slug>", methods=["GET"], endpoint="por_categoria")
def por_categoria(cat_id, slug):
    cat = Categoria.query.get_or_404(cat_id)
    expected_slug = slugify(cat.nombre)
    if slug != expected_slug:
        return redirect(url_for("negocios.por_categoria", cat_id=cat.id, slug=expected_slug), code=301)

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 12, type=int), 30)

    query = (Negocio.query.options(joinedload(Negocio.categoria))
             .filter_by(categoria_id=cat.id, estado="aprobado")
             .order_by(Negocio.nombre.asc()))
    pag = query.paginate(page=page, per_page=per_page, error_out=False)

    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    return render_template("negocios/por_categoria.html",
                           categoria=cat, categorias=categorias,
                           negocios=pag.items, pag=pag)


# ----------------------------------------------------
# 🔹 Detalle (vista individual)
# ----------------------------------------------------
@negocios_bp.route("/<int:id>", methods=["GET"], endpoint="detalle")
def detalle(id):
    negocio = Negocio.query.get_or_404(id)

    # Buscar perfil de empresa o usuario asociado
    perfil = None
    if negocio.usuario and hasattr(negocio.usuario, "perfil"):
        perfil = negocio.usuario.perfil
    elif hasattr(negocio, "usuario") and hasattr(negocio.usuario, "perfil_empresa"):
        perfil = negocio.usuario.perfil_empresa

    feed = []

    # ------------- Avisos -------------
    for a in getattr(perfil, "avisos", []) if perfil else []:
        feed.append({
            "tipo": "aviso",
            "fecha": a.fecha_inicio or a.fecha_fin or date.today(),
            "titulo": "Aviso",
            "descripcion": a.mensaje or "",
            "imagen": getattr(a, "imagen", None),
            "extra": {"inicio": a.fecha_inicio, "fin": a.fecha_fin}
        })

    # ------------- Eventos -------------
    for e in getattr(perfil, "eventos", []) if perfil else []:
        feed.append({
            "tipo": "evento",
            "fecha": e.fecha or date.today(),
            "titulo": e.titulo,
            "descripcion": e.descripcion or "",
            "imagen": getattr(e, "imagen", None),
            "extra": {"fecha": e.fecha, "lugar": getattr(e, "lugar", None)}
        })

    # ------------- Noticias -------------
    for n in getattr(perfil, "noticias", []) if perfil else []:
        feed.append({
            "tipo": "noticia",
            "fecha": getattr(n, "fecha", date.today()),
            "titulo": n.titulo,
            "descripcion": n.contenido or "",
            "imagen": getattr(n, "imagen", None),
            "extra": {"fecha": getattr(n, "fecha", None)}
        })

    # ------------- Ofertas -------------
    for o in getattr(perfil, "ofertas", []) if perfil else []:
        vigente_flag = None
        if hasattr(o, "vigente"):
            try:
                vigente_flag = o.vigente() if callable(o.vigente) else bool(o.vigente)
            except Exception:
                vigente_flag = None
        feed.append({
            "tipo": "oferta",
            "fecha": o.fecha_inicio or date.today(),
            "titulo": getattr(o, "titulo", None) or "Oferta",
            "descripcion": getattr(o, "descripcion", "") or "",
            "imagen": getattr(o, "imagen", None),
            "extra": {
                "inicio": getattr(o, "fecha_inicio", None),
                "fin": getattr(o, "fecha_fin", None),
                "vigente": vigente_flag
            }
        })

    # Ordenar por fecha (más reciente primero)
    feed.sort(key=lambda x: x.get("fecha") or date.today(), reverse=True)

    return render_template("negocios/detalle.html", negocio=negocio, perfil=perfil, feed=feed)


# ----------------------------------------------------
# 🔹 Registrar nuevo negocio
# ----------------------------------------------------
@negocios_bp.route("/registrar", methods=["GET", "POST"], endpoint="registrar")
@login_required
def registrar():
    if Negocio.query.filter_by(usuario_id=current_user.id).first():
        flash("⚠️ Solo puedes registrar un negocio. Adminístralo desde tu perfil.", "warning")
        return redirect(url_for("ciudadano.dashboard"))

    # Crear categorías iniciales si no existen
    if not Categoria.query.first():
        iniciales = [
            "Minimarkets y Almacenes", "Supermercados", "Ferreterías", "Tiendas de ropa y calzado",
            "Restaurantes", "Comida rápida", "Cafeterías", "Panaderías y pastelerías", "Farmacias",
            "Consultorios médicos", "Dentistas", "Gimnasios", "Abogados", "Contadores", "Ingenieros",
            "Servicios informáticos", "Colectivos y Taxis", "Talleres mecánicos", "Venta de repuestos",
            "Constructoras", "Electricistas", "Gasfitería", "Pintores", "Jardines infantiles",
            "Escuelas y liceos", "Preuniversitarios", "Eventos y banquetería", "Fotografía y video",
            "Turismo local", "Veterinarias", "Tiendas de mascotas", "Peluquería canina",
            "Municipalidad", "Bancos y cajas de compensación", "Correos y encomiendas"
        ]
        db.session.bulk_save_objects([Categoria(nombre=n) for n in iniciales])
        db.session.commit()
        flash("⚡ Categorías iniciales creadas automáticamente.", "info")

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


# ----------------------------------------------------
# 🔹 Fallback simple (listado por categoría)
# ----------------------------------------------------
@negocios_bp.route("/categoria/simple/<int:id>", methods=["GET"], endpoint="por_categoria_simple")
def negocios_por_categoria_simple(id):
    categoria = Categoria.query.get_or_404(id)
    negocios = (Negocio.query.filter_by(categoria_id=id, estado="aprobado")
                .order_by(Negocio.nombre.asc()).all())
    return render_template("negocios/por_categoria.html", categoria=categoria, negocios=negocios)
