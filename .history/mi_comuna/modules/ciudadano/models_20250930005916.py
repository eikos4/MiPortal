# mi_comuna/modules/ciudadano/models.py

from mi_comuna.extensions import db
from datetime import datetime


class PerfilEmpresa(db.Model):
    __tablename__ = "perfil_empresa"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False, unique=True, index=True)

    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    sitio_web = db.Column(db.String(255), nullable=True)
    facebook = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    tiktok = db.Column(db.String(255), nullable=True)
    horario = db.Column(db.String(255), nullable=True)
    logo = db.Column(db.String(255), nullable=True)  # Logo/imagen empresa

    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=True)
    categoria = db.relationship("Categoria", backref="perfiles")

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PerfilEmpresa {self.nombre} ({self.usuario_id})>"


class Evento(db.Model):
    __tablename__ = "evento_ciudadano"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    fecha_inicio = db.Column(db.Date, nullable=False, index=True)
    fecha_fin = db.Column(db.Date, nullable=True, index=True)
    lugar = db.Column(db.String(255), nullable=True)
    imagen = db.Column(db.String(255), nullable=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False, index=True)
    perfil = db.relationship("PerfilEmpresa", backref="eventos")

    def __repr__(self):
        return f"<Evento {self.titulo} ({self.perfil_id})>"


class Aviso(db.Model):
    __tablename__ = "aviso_ciudadano"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False, index=True)
    perfil = db.relationship("PerfilEmpresa", backref="avisos")

    def __repr__(self):
        return f"<Aviso {self.titulo} ({self.perfil_id})>"



class NoticiaEmpresa(db.Model):
    __tablename__ = "noticia_empresa"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)

    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False, index=True)
    perfil = db.relationship("PerfilEmpresa", backref="noticias")

    def __repr__(self):
        return f"<NoticiaEmpresa {self.titulo} ({self.perfil_id})>"


class Oferta(db.Model):
    __tablename__ = "oferta"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)

    fecha_inicio = db.Column(db.Date, nullable=True, index=True)
    fecha_fin = db.Column(db.Date, nullable=True, index=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False, index=True)
    perfil = db.relationship("PerfilEmpresa", backref="ofertas")

    def vigente(self):
        """Devuelve True si la oferta sigue activa hoy."""
        hoy = datetime.utcnow().date()
        if self.fecha_inicio and self.fecha_inicio > hoy:
            return False
        if self.fecha_fin and self.fecha_fin < hoy:
            return False
        return True

    def __repr__(self):
        return f"<Oferta {self.titulo} ({self.perfil_id})>"
