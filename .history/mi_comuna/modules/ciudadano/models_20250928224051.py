from mi_comuna.extensions import db

class PerfilEmpresa(db.Model):
    __tablename__ = "perfil_empresa"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    # relaciones
    usuario = db.relationship("Usuario", backref="perfil_empresa", uselist=False)

class Evento(db.Model):
    __tablename__ = "evento_ciudadano"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="eventos")

class Aviso(db.Model):
    __tablename__ = "aviso_ciudadano"
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(255), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="avisos")

class NoticiaEmpresa(db.Model):
    __tablename__ = "noticia_empresa"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="noticias")

class Oferta(db.Model):
    __tablename__ = "oferta"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    imagen = db.Column(db.String(255), nullable=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("perfil_empresa.id"), nullable=False)
    empresa = db.relationship("PerfilEmpresa", backref="ofertas")
