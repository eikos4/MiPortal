from mi_comuna.extensions import db
from datetime import datetime

class PerfilEmpresa(db.Model):
    __tablename__ = "perfil_empresa"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False, unique=True)
    nombre_comercial = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    sitio_web = db.Column(db.String(255), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)

    usuario = db.relationship("Usuario", backref="perfil_empresa", uselist=False)


from mi_comuna.extensions import db
from datetime import datetime

from mi_comuna.extensions import db
from datetime import datetime

class Evento(db.Model):
    __tablename__ = "evento"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    hora = db.Column(db.Time, nullable=True)
    lugar = db.Column(db.String(200), nullable=True)

    # Si es un evento de empresa
    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=True)

    # Tipo de evento: "municipal" o "empresa"
    tipo = db.Column(db.String(20), default="municipal")

    empresa = db.relationship("PerfilEmpresa", backref="eventos", lazy=True)



class Aviso(db.Model):
    __tablename__ = "aviso"
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(255), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)

    empresa = db.relationship("PerfilEmpresa", backref="avisos")


class NoticiaEmpresa(db.Model):
    __tablename__ = "noticia_empresa"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)

    empresa = db.relationship("PerfilEmpresa", backref="noticias")


class Oferta(db.Model):
    __tablename__ = "oferta"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime, nullable=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="ofertas")
