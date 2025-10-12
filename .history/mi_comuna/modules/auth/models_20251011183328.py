from mi_comuna.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default="ciudadano", nullable=False)  # admin | ciudadano | otro

    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)


    # -----------------------------------------------------------------
    # Métodos de autenticación
    # -----------------------------------------------------------------
    def set_password(self, password: str) -> None:
        """Genera un hash seguro para la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica si la contraseña coincide con el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    # -----------------------------------------------------------------
    # Métodos de utilidad
    # -----------------------------------------------------------------
    def __repr__(self):
        return f"<Usuario {self.email} ({self.rol})>"


# ---------------------------------------------------------------------
# Flask-Login: carga de usuario por ID
# ---------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    """Función que indica a Flask-Login cómo cargar un usuario desde su ID."""
    return Usuario.query.get(int(user_id))
