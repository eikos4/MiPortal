# mi_comuna/modules/auth/routes.py
from urllib.parse import urlparse
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from . import auth_bp
from .models import Usuario
from .forms import LoginForm, RegisterForm
from mi_comuna.extensions import db

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Ya has iniciado sesión.", "info")
        return redirect(url_for("inicio.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        existente = Usuario.query.filter_by(email=form.email.data.strip().lower()).first()
        if existente:
            flash("⚠️ Este correo ya está registrado. Inicia sesión.", "warning")
            return redirect(url_for("auth.login"))
        nuevo = Usuario(
            nombre=form.nombre.data.strip(),
            email=form.email.data.strip().lower(),
            rol="ciudadano",
        )
        nuevo.set_password(form.password.data)
        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Cuenta creada con éxito. Ahora inicia sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Ya has iniciado sesión.", "info")
        return redirect(url_for("inicio.index"))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.strip().lower()).first()
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario, remember=getattr(form, "remember_me", None) and form.remember_me.data)
            flash("✅ Sesión iniciada correctamente.", "success")

            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                # Redirección por rol
                if usuario.rol == "admin":
                    next_page = url_for("admin.dashboard")
                elif usuario.rol == "ciudadano":
                    next_page = url_for("ciudadano.dashboard")
                else:
                    next_page = url_for("inicio.index")
            return redirect(next_page)
        flash("❌ Credenciales inválidas. Verifica tu correo o contraseña.", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("👋 Sesión cerrada correctamente.", "info")
    return redirect(url_for("inicio.index"))
