from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

# ---------------------------------------------------------------------
# Inicialización de extensiones
# ---------------------------------------------------------------------
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

# ---------------------------------------------------------------------
# Configuración del LoginManager
# ---------------------------------------------------------------------
# Esta configuración se completará en create_app(),
# pero dejamos los valores por defecto para evitar errores.
login_manager.login_view = "auth.login"
login_manager.login_message = "⚠️ Debes iniciar sesión para acceder."
login_manager.login_message_category = "warning"
