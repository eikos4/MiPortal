import os

class Config:
    SECRET_KEY = "dev_secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///mi_comuna.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    UPLOAD_FOLDER = os.path.join("mi_comuna", "static", "uploads")
    UPLOAD_URL_PREFIX = "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size