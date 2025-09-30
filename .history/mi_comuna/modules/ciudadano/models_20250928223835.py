from mi_comuna.extensions import db
from datetime import datetime

class PerfilEmpresa(db.Model):
    __tablename__ = "perfil_empresa"

    id = db.Column(db.Integer, primary_key=True)
    nombre_comercial = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(50), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    usuario = db.relationship("Usuario", backref="perfil_empresa", uselist=False)


class EventoEmpresa(db.Model):
    __tablename__ = "evento_empresa"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    lugar = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="eventos", lazy=True)


class Aviso(db.Model):
    __tablename__ = "aviso_empresa"

    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(255), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime, nullable=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="avisos", lazy=True)


class NoticiaEmpresa(db.Model):
    __tablename__ = "noticia_empresa"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="noticias", lazy=True)


class Oferta(db.Model):
    __tablename__ = "oferta_empresa"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime, nullable=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="ofertas", lazy=True)
