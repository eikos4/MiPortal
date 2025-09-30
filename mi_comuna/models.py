# Modelos globales (ej: Usuario, Rol, Comuna)
from flask_login import UserMixin
from .extensions import db
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default="user")  # user | admin

