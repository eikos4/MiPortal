# mi_comuna/__init__.py
from flask import Flask
from mi_comuna.extensions import db, migrate, login_manager, csrf
from config import Config
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Blueprints
    from mi_comuna.modules.auth import auth_bp
    from mi_comuna.modules.ciudadano import ciudadano_bp
    from mi_comuna.modules.admin import admin_bp
    from mi_comuna.modules.negocios import negocios_bp
    from mi_comuna.modules.inicio import inicio_bp

    app.register_blueprint(auth_bp)                 # /login, /register, /logout
    app.register_blueprint(ciudadano_bp, url_prefix="/ciudadano")
    app.register_blueprint(admin_bp, url_prefix="/admin")      # coincide con el del módulo
    app.register_blueprint(negocios_bp, url_prefix="/negocios")
    app.register_blueprint(inicio_bp, url_prefix="/")

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow, "current_year": datetime.utcnow().year}

    with app.app_context():
        db.create_all()

    return app
