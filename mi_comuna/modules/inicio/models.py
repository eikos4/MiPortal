from datetime import datetime
from mi_comuna.extensions import db


# ---------------------------------------------------------------------
# 📰 Noticia
# ---------------------------------------------------------------------
class Noticia(db.Model):
    __tablename__ = "noticia"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)


# ---------------------------------------------------------------------
# 📢 Aviso
# ---------------------------------------------------------------------
class Aviso(db.Model):
    __tablename__ = "aviso"

    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(500), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    imagen = db.Column(db.String(255), nullable=True)


# ---------------------------------------------------------------------
# 🎉 Evento
# ---------------------------------------------------------------------
class Evento(db.Model):
    __tablename__ = "evento"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    lugar = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    imagen = db.Column(db.String(255), nullable=True)
