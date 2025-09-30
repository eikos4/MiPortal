from mi_comuna import create_app
from mi_comuna.extensions import db
from mi_comuna.modules.auth.models import Usuario

app = create_app()
with app.app_context():
    # Crear usuario admin
    admin = Usuario(
        nombre="Administrador",
        email="admin@parral.cl",
        rol="admin"
    )
    admin.set_password("123456")  # 👈 usamos tu método set_password
    
    db.session.add(admin)
    db.session.commit()
    print("✅ Usuario admin creado: admin@parral.cl / 123456")
