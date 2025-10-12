from mi_comuna import create_app
from mi_comuna.extensions import db
from mi_comuna.modules.auth.models import Usuario

app = create_app()
with app.app_context():
    nombre = input("Nombre admin: ") or "Admin"
    email = input("Correo admin: ") or "admin@miportal.cl"
    password = input("Password admin: ") or "admin123"
    if Usuario.query.filter_by(email=email.lower()).first():
        print("⚠️ Ya existe ese correo.")
    else:
        u = Usuario(nombre=nombre, email=email.lower(), rol="admin")
        u.set_password(password)
        db.session.add(u); db.session.commit()
        print("✅ Admin creado.")
