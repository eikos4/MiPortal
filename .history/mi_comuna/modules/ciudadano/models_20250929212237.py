# mi_comuna/modules/ciudadano/models.py

from mi_comuna.extensions import db
from datetime import datetime


class PerfilEmpresa(db.Model):
    __tablename__ = "perfil_empresa"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=True)
    redes = db.Column(db.String(255), nullable=True)

    # relación 1:1 con usuario
    usuario = db.relationship("Usuario", backref="perfil_empresa", uselist=False)


class Evento(db.Model):
    __tablename__ = "evento_ciudadano"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    lugar = db.Column(db.String(255), nullable=True)
    imagen = db.Column(db.String(255), nullable=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="eventos")


class Aviso(db.Model):
    __tablename__ = "aviso_ciudadano"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="avisos")


class NoticiaEmpresa(db.Model):
    __tablename__ = "noticia_empresa"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    fecha_publicacion = db.Column(db.Date, default=datetime.utcnow)

    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="noticias")


class Oferta(db.Model):
    __tablename__ = "oferta"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="ofertas")
