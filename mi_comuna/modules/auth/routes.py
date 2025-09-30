from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from .models import Usuario
from .forms import LoginForm, RegisterForm
from mi_comuna.extensions import db

# ----------------------------
# Registro de usuarios
# ----------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nuevo = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            rol="ciudadano"  # 👈 por defecto, los nuevos son ciudadanos
        )
        nuevo.set_password(form.password.data)
        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Cuenta creada con éxito. Ahora inicia sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


# ----------------------------
# Login
# ----------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario)
            flash("✅ Sesión iniciada correctamente", "success")

            # Redirecciones según rol
            if usuario.rol == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            elif usuario.rol == "ciudadano":
                return redirect(url_for("ciudadano.dashboard"))
            else:
                return redirect(url_for("inicio.index"))

        flash("❌ Credenciales inválidas", "danger")

    return render_template("auth/login.html", form=form)


# ----------------------------
# Logout
# ----------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for("inicio.index"))
