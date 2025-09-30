from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import negocios_bp
from .forms import NegocioForm
from .models import Negocio
from mi_comuna.extensions import db
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.path.join("mi_comuna", "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@negocios_bp.route("/registrar", methods=["GET", "POST"])
@login_required
def registrar():
    form = NegocioForm()
    form.categoria_id.choices = categorias_defecto

    if form.validate_on_submit():
        filename = None
        if form.imagen.data:
            filename = secure_filename(form.imagen.data.filename)
            form.imagen.data.save(os.path.join(UPLOAD_FOLDER, filename))

        nuevo = Negocio(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            direccion=form.direccion.data,
            telefono=form.telefono.data,
            whatsapp=form.whatsapp.data,
            redes=form.redes.data,
            categoria_id=form.categoria_id.data,
            usuario_id=current_user.id,
            estado="pendiente",
            imagen=f"uploads/{filename}" if filename else None
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Tu negocio fue registrado y está pendiente de aprobación.", "success")
        return redirect(url_for("negocios.lista"))

    return render_template("negocios/register.html", form=form)
