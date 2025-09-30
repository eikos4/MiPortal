# ---------------------------
# Registrar negocio
# ---------------------------
from flask import redirect, render_template
from flask_login import current_user


@negocios_bp.route("/registrar", methods=["GET", "POST"], endpoint="registrar")
@login_required
def registrar():
    # 🚨 Bloqueo: usuario ya tiene negocio
    negocio_existente = Negocio.query.filter_by(usuario_id=current_user.id).first()
    if negocio_existente:
        flash("⚠️ Solo puedes registrar un negocio. Adminístralo desde tu perfil.", "warning")
        return redirect(url_for("ciudadano.dashboard"))

    # ⚡ Crear categorías iniciales si no existen
    if not Categoria.query.first():
        iniciales = [
            "Minimarkets y Almacenes", "Supermercados", "Ferreterías",
            "Restaurantes", "Cafeterías", "Panaderías y pastelerías",
            "Farmacias", "Consultorios médicos", "Dentistas",
            "Talleres mecánicos", "Constructoras", "Electricistas"
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
            imagen_rel = save_image(form.imagen.data) if form.imagen.data else None
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("negocios/register.html", form=form, categorias=categorias_db)

        # 🔹 Crear perfil empresa si no existe
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
        return redirect(url_for("ciudadano.dashboard"))

    return render_template("negocios/register.html", form=form, categorias=categorias_db)
