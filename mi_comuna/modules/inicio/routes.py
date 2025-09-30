from flask import render_template
from . import inicio_bp
from .models import Noticia, Aviso, Evento
from mi_comuna.modules.negocios.models import Negocio
from mi_comuna.modules.auth.models import Usuario

@inicio_bp.route("/")
def index():
    noticias = Noticia.query.limit(3).all()
    avisos = Aviso.query.limit(3).all()
    eventos = Evento.query.limit(3).all()

    # 📊 estadísticas rápidas
    stats = {
        "negocios": Negocio.query.filter_by(estado="aprobado").count(),
        "usuarios": Usuario.query.count(),
        "resenas": 0  # cuando agregues modelo de reseñas lo reemplazamos
    }

    # ⭐ negocios destacados (ej: últimos aprobados)
    negocios = Negocio.query.filter_by(estado="aprobado").limit(6).all()

    return render_template(
        "inicio/index.html",
        noticias=noticias,
        avisos=avisos,
        eventos=eventos,
        stats=stats,
        negocios=negocios
    )

@inicio_bp.route("/noticias")
def noticias():
    noticias = Noticia.query.all()
    return render_template("inicio/noticias.html", noticias=noticias)

@inicio_bp.route("/noticia/<int:id>")
def ver_noticia(id):
    noticia = Noticia.query.get_or_404(id)
    return render_template("inicio/ver_noticia.html", noticia=noticia)


@inicio_bp.route("/avisos")
def avisos():
    avisos = Aviso.query.all()
    return render_template("inicio/avisos.html", avisos=avisos)

@inicio_bp.route("/eventos")
def eventos():
    eventos = Evento.query.all()
    return render_template("inicio/eventos.html", eventos=eventos)
