from mi_comuna import create_app

app = create_app()
from flask_wtf import CSRFProtect

csrf = CSRFProtect()
csrf.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
