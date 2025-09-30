from mi_comuna.extensions import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    icono = db.Column(db.String(100), nullable=True)  # opcional para UI
    negocios = db.relationship("Negocio", backref="categoria", lazy=True)

class Negocio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(50), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=True)
    redes = db.Column(db.String(200), nullable=True)
    horarios = db.Column(db.String(200), nullable=True)
    estado = db.Column(db.String(50), default="pendiente")  # pendiente, aprobado, rechazado

    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))  # dueño del negocio
