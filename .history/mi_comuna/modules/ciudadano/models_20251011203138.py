# mi_comuna/modules/ciudadano/models.py
from datetime import datetime, date
from mi_comuna.extensions import db


# ======================================================
# 🏢 Perfil de Empresa / Emprendedor
# ======================================================
class PerfilEmpresa(db.Model):
    __tablename__ = "perfil_empresa"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(50))
    whatsapp = db.Column(db.String(50))
    email = db.Column(db.String(120))
    sitio_web = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    tiktok = db.Column(db.String(255))
    horario = db.Column(db.String(255))
    logo = db.Column(db.String(255))

    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id", ondelete="SET NULL"))
    categoria = db.relationship("Categoria", backref="perfiles")

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PerfilEmpresa {self.nombre} (usuario_id={self.usuario_id})>"

    @property
    def total_publicaciones(self):
        """Cantidad total de contenidos publicados (noticias + avisos + eventos + ofertas)."""
        return len(self.noticias) + len(self.avisos) + len(self.eventos) + len(self.ofertas)


# ======================================================
# 🎉 Evento publicado por empresa (CIUDADANO)
# ======================================================
class EventoCiudadano(db.Model):
    __tablename__ = "evento_ciudadano"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    fecha_inicio = db.Column(db.Date, nullable=False, index=True)
    fecha_fin = db.Column(db.Date, index=True)
    lugar = db.Column(db.String(255))
    imagen = db.Column(db.String(255))

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id", ondelete="CASCADE"), nullable=False, index=True)
    perfil = db.relationship(
        "PerfilEmpresa",
        backref=db.backref("eventos", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<EventoCiudadano {self.titulo} (perfil_id={self.perfil_id})>"

    @property
    def activo(self):
        """Devuelve True si el evento aún está vigente."""
        hoy = date.today()
        return (self.fecha_fin is None) or (self.fecha_fin >= hoy)


# ======================================================
# 📢 Aviso de empresa (CIUDADANO)
# ======================================================
class AvisoCiudadano(db.Model):
    __tablename__ = "aviso_ciudadano"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255))

    creado_en = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id", ondelete="CASCADE"), nullable=False, index=True)
    perfil = db.relationship(
        "PerfilEmpresa",
        backref=db.backref("avisos", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<AvisoCiudadano {self.titulo} (perfil_id={self.perfil_id})>"


# ======================================================
# 📰 Noticia de empresa (CIUDADANO)
# ======================================================
class NoticiaEmpresa(db.Model):
    __tablename__ = "noticia_empresa"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255))

    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id", ondelete="CASCADE"), nullable=False, index=True)
    perfil = db.relationship(
        "PerfilEmpresa",
        backref=db.backref("noticias", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<NoticiaEmpresa {self.titulo} (perfil_id={self.perfil_id})>"

    @property
    def resumen(self):
        """Devuelve un resumen corto del contenido."""
        if not self.contenido:
            return ""
        return (self.contenido[:120] + "…") if len(self.contenido) > 120 else self.contenido


# ======================================================
# 💰 Oferta comercial (CIUDADANO)
# ======================================================
class OfertaCiudadano(db.Model):
    __tablename__ = "oferta_ciudadano"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255))

    fecha_inicio = db.Column(db.Date, index=True)
    fecha_fin = db.Column(db.Date, index=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id", ondelete="CASCADE"), nullable=False, index=True)
    perfil = db.relationship(
        "PerfilEmpresa",
        backref=db.backref("ofertas", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<OfertaCiudadano {self.titulo} (perfil_id={self.perfil_id})>"

    @property
    def vigente(self):
        """Devuelve True si la oferta está actualmente activa."""
        hoy = date.today()
        if self.fecha_inicio and self.fecha_inicio > hoy:
            return False
        if self.fecha_fin and self.fecha_fin < hoy:
            return False
        return True
