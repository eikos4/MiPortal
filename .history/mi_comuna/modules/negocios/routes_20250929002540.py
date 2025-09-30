from flask import render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import os, uuid, re
from datetime import datetime

from . import negocios_bp
from .models import Negocio, Categoria
from .forms import NegocioForm
from mi_comuna.extensions import db

# 🔹 Importamos PerfilEmpresa para sincronizar con el módulo ciudadano
from mi_comuna.modules.ciudadano.models import PerfilEmpresa


# ---------------------------
# Helpers
# ---------------------------
def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def allowed_file(filename):
    allowed = {"png", "jpg", "jpeg", "webp", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


def save_image(file_storage):
    if not file_storage or file_storage.filename == "":
        return None
    if not allowed_file(file_storage.filename):
        raise ValueError("Formato de imagen no permitido.")
    filename = secure_filename(file_storage.filename)
    unique = f"{uuid.uuid4().hex}_{filename}"  # nombre único
    upload_root = current_app.config.get("UPLOAD_FOLDER") or os.path.join("mi_comuna", "static", "uploads")
    os.makedirs(upload_root, exist_ok=True)
    path = os.path.join(upload_root, unique)
    file_storage.save(path)
    static_prefix = current_app.config.get("UPLOAD_URL_PREFIX", "uploads")
    return f"{static_prefix}/{unique}"


# ---------------------------
# Listado de negocios
# ---------------------------
@negocios_bp.route("/", endpoint="lista")
def lista_negocios():
    q = request.args.get("q", "", type=str).strip()
    categoria_id = request.args.get("categoria", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 9, type=int), 30)

    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()

    # Si hay filtros
    if q or categoria_id:
        query = (Negocio.query
                 .options(joinedload(Negocio.categoria))
                 .filter(Negocio.estado == "aprobado"))

        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    Negocio.nombre.ilike(like),
                    Negocio.descripcion.ilike(like),
                    Negocio.direccion.ilike(like)
                )
            )

        if categoria_id:
            query = query.filter(Negocio.categoria_id == categoria_id)

        query = query.order_by(Negocio.nombre.asc())
        pag = query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template(
            "negocios/lista.html",
            categorias=categorias,
            negocios=pag.items,
            pag=pag,
            q=q,
            categoria_actual=categoria_id,
            top_por_categoria=None
        )

    # Si NO hay filtros: Top 3 por categoría
    top_por_categoria = []
    for cat in categorias:
        top = (Negocio.query
               .options(joinedload(Negocio.categoria))
               .filter_by(categoria_id=cat.id, estado="aprobado")
               .order_by(Negocio.id.desc())
               .limit(3)
               .all())
        if top:
            top_por_categoria.append({
                "categoria": cat,
                "slug": slugify(cat.nombre),
                "negocios": top
            })

    return render_template(
        "negocios/lista.html",
        categorias=categorias,
        top_por_categoria=top_por_categoria,
        negocios=None,
        pag=None,
        q="",
        categoria_actual=None
    )


# ---------------------------
# Vista de categoría
# ---------------------------
@negocios_bp.route("/categoria/<int:cat_id>-<slug>")
def por_categoria(cat_id, slug):
    cat = Categoria.query.get_or_404(cat_id)
    if slugify(cat.nombre) != slug:
        return redirect(url_for("negocios.por_categoria", cat_id=cat_id, slug=slugify(cat.nombre)), code=301)

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 12, type=int), 30)

    query = (Negocio.query
             .options(joinedload(Negocio.categoria))
             .filter_by(categoria_id=cat.id, estado="aprobado")
             .order_by(Negocio.nombre.asc()))
    pag = query.paginate(page=page, per_page=per_page, error_out=False)

    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()

    return render_template(
        "negocios/por_categoria.html",
        categoria=cat,
        categorias=categorias,
        negocios=pag.items,
        pag=pag
    )


# ---------------------------
# Detalle
# ---------------------------
@negocios_bp.route("/<int:id>", methods=["GET"], endpoint="detalle")
def detalle(id):
    negocio = (Negocio.query
               .options(joinedload(Negocio.categoria))
               .get_or_404(id))

    relacionados = []
    if negocio.categoria_id:
        relacionados = (Negocio.query
                        .filter(Negocio.id != negocio.id,
                                Negocio.estado == "aprobado",
                                Negocio.categoria_id == negocio.categoria_id)
                        .order_by(Negocio.id.desc())
                        .limit(3)
                        .all())

    return render_template("negocios/detalle.html", negocio=negocio, relacionados=relacionados)


# ---------------------------
# Registrar negocio
# ---------------------------
@negocios_bp.route("/registrar", methods=["GET", "POST"], endpoint="registrar")
@login_required
def registrar():
    # ⚡ Si no hay categorías, creamos las iniciales
    if not Categoria.query.first():
        iniciales = [
            "Minimarkets y Almacenes", "Supermercados", "Ferreterías", "Tiendas de ropa y calzado",
            "Restaurantes", "Comida rápida", "Cafeterías", "Panaderías y pastelerías",
            "Farmacias", "Consultorios médicos", "Dentistas", "Gimnasios",
            "Abogados", "Contadores", "Ingenieros", "Servicios informáticos",
            "Colectivos y Taxis", "Talleres mecánicos", "Venta de repuestos",
            "Constructoras", "Electricistas", "Gasfitería", "Pintores",
            "Jardines infantiles", "Escuelas y liceos", "Preuniversitarios",
            "Eventos y banquetería", "Fotografía y video", "Turismo local",
            "Veterinarias", "Tiendas de mascotas", "Peluquería canina",
            "Municipalidad", "Bancos y cajas de compensación", "Correos y encomiendas"
        ]
        for nombre in iniciales:
            db.session.add(Categoria(nombre=nombre))
        db.session.commit()
        flash("⚡ Categorías iniciales creadas automáticamente.", "info")

    form = NegocioForm()
    categorias_db = Categoria.query.order_by(Categoria.nombre.asc()).all()
    form.categoria_id.choices = [(c.id, c.nombre) for c in categorias_db]

    if form.validate_on_submit():
        try:
            imagen_rel = save_image(form.imagen.data) if getattr(form, "imagen", None) else None
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("negocios/register.html", form=form, categorias=categorias_db)

        # 🔹 Crear perfil de empresa si no existe
        perfil = PerfilEmpresa.query.filter_by(usuario_id=current_user.id).first()
        if not perfil:
            perfil = PerfilEmpresa(
                usuario_id=current_user.id,
                nombre=form.nombre.data.strip(),
                descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
                direccion=form.direccion.data.strip()
            )
            db.session.add(perfil)
            db.session.commit()

        # 🔹 Registrar negocio
        nuevo = Negocio(
            nombre=form.nombre.data.strip(),
            descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
            direccion=form.direccion.data.strip(),
            telefono=form.telefono.data.strip() if form.telefono.data else None,
            whatsapp=form.whatsapp.data.strip() if form.whatsapp.data else None,
            redes=form.redes.data.strip() if form.redes.data else None,
            horario=form.horario.data.strip() if form.horario.data else None,
            categoria_id=form.categoria_id.data,
            usuario_id=current_user.id,
            estado="pendiente",
            imagen=imagen_rel
        )
        db.session.add(nuevo)
        db.session.commit()

        flash("✅ Tu negocio fue registrado y está pendiente de aprobación.", "success")
        return redirect(url_for("ciudadano.dashboard"))  # 👈 redirige al dashboard ciudadano

    return render_template("negocios/register.html", form=form, categorias=categorias_db)
