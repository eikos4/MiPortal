from datetime import datetime
from flask import Flask
from .extensions import db, migrate, login_manager
from .modules.inicio import inicio_bp, models as inicio_models
from .modules.auth import auth_bp, models as auth_models   # 👈 nuevo
from .modules.negocios import negocios_bp, models as negocios_models      # 👈 nuevo
from .modules.admin import admin_bp 
from .modules.ciudadano import ciudadano_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # User loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return auth_models.Usuario.query.get(int(user_id))
    
    @app.context_processor
    def inject_now():
        return {"now": datetime.now}

    # Blueprints
    app.register_blueprint(inicio_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(negocios_bp, url_prefix="/negocios")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(ciudadano_bp)



    return app


