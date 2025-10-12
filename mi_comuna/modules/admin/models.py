from mi_comuna.extensions import db

class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    icono = db.Column(db.String(100), nullable=True)  # opcional para UI

    # relación bidireccional
    negocios = db.relationship("Negocio", back_populates="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.nombre}>"


class Negocio(db.Model):
    __tablename__ = "negocio"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(50), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=True)
    redes = db.Column(db.String(200), nullable=True)
    horarios = db.Column(db.String(200), nullable=True)
    imagen = db.Column(db.String(255), nullable=True)  # útil para mostrar logo/foto

    # estado de revisión
    estado = db.Column(
        db.String(20),
        default="pendiente",
        nullable=False,
        doc="pendiente | aprobado | rechazado"
    )

    # relaciones
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    categoria = db.relationship("Categoria", back_populates="negocios", lazy=True)
    usuario = db.relationship("Usuario", backref="negocios", lazy=True)

    def __repr__(self):
        return f"<Negocio {self.nombre} - Estado: {self.estado}>"
