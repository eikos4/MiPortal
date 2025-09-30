from flask import Blueprint, render_template

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/')
def list():
    cursos_mock = [
        {"titulo": "Álgebra I", "profesor": "María Soto"},
        {"titulo": "Física para principiantes", "profesor": "Juan Pérez"},
        {"titulo": "Programación en Python", "profesor": "Ana Torres"},
    ]
    return render_template('courses/list.html', cursos=cursos_mock)
