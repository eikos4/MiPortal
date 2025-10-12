import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # -----------------------
    # 🔐 Seguridad
    # -----------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")  # usa variable de entorno en prod

    # -----------------------
    # 🗃️ Base de datos
    # -----------------------
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'mi_comuna.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------
    # 📂 Archivos subidos
    # -----------------------
    # Definir la ruta base de la aplicación
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

        # Configurar la carpeta de carga de archivos
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "mi_comuna", "static", "uploads")

        # Configurar el prefijo de la URL para acceder a los archivos
    UPLOAD_URL_PREFIX = "uploads"

        # Limitar el tamaño máximo de carga a 16 MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # -----------------------
    # 🌐 Configuración del sitio
    # -----------------------
    SITE_NAME = "Mi Portal Parral"
    MUNICIPALITY_NAME = "Municipalidad de Parral"
    DEFAULT_LANGUAGE = "es"

    # -----------------------
    # 🔒 Sesiones / Cookies
    # -----------------------
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # cambia a True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # -----------------------
    # 📧 Email (opcional si integras notificaciones)
    # -----------------------
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@miportal.cl")
