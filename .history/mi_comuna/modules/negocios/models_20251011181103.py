from mi_comuna.extensions import db

class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    icono = db.Column(db.String(100), nullable=True)  # opcional para UI

    # Relación uno-a-muchos con Negocio
    negocios = db.relationship("Negocio", backref="categoria", lazy=True)


class Negocio(db.Model):
    __tablename__ = "negocio"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(50), nullable=True)
    whatsapp = db.Column(db.String(50), nullable=True)
    redes = db.Column(db.String(255), nullable=True)
    horarios = db.Column(db.String(120), nullable=True)  # 👈 cambia "horario" → "horarios"
    imagen = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.String(20), default="pendiente")

    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False, unique=True)

    usuario = db.relationship("Usuario", backref="negocio", uselist=False)


    @property
    def imagen_url(self):
        """Devuelve la URL completa o una imagen por defecto."""
        from flask import url_for
        return url_for("static", filename=self.imagen) if self.imagen else url_for("static", filename="img/logo.png")

