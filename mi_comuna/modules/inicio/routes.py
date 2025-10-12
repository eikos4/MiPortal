from datetime import date
from flask import render_template
from . import inicio_bp
from .models import Noticia, Aviso, Evento
from mi_comuna.modules.negocios.models import Negocio
from mi_comuna.modules.auth.models import Usuario


# ---------------------------------------------------------------------
# Página principal
# ---------------------------------------------------------------------
@inicio_bp.route("/")
def index():
    """Portada con últimas noticias, eventos, avisos y estadísticas generales."""
    noticias = (
        Noticia.query.order_by(Noticia.fecha.desc())
        .limit(3)
        .all()
    )

    hoy = date.today()
    avisos = (
        Aviso.query
        .filter(Aviso.fecha_inicio <= hoy)
        .filter((Aviso.fecha_fin == None) | (Aviso.fecha_fin >= hoy))
        .order_by(Aviso.fecha_inicio.desc())
        .limit(3)
        .all()
    )

    eventos = (
        Evento.query.order_by(Evento.fecha.desc())
        .limit(3)
        .all()
    )

    # 📊 estadísticas rápidas
    stats = {
        "negocios": Negocio.query.filter_by(estado="aprobado").count(),
        "usuarios": Usuario.query.count(),
        "resenas": 0  # Placeholder, se actualizará cuando se agregue el modelo de reseñas
    }

    # ⭐ Negocios destacados: últimos aprobados
    negocios = (
        Negocio.query.filter_by(estado="aprobado")
        .order_by(Negocio.id.desc())
        .limit(6)
        .all()
    )

    return render_template(
        "inicio/index.html",
        noticias=noticias,
        avisos=avisos,
        eventos=eventos,
        stats=stats,
        negocios=negocios,
    )


# ---------------------------------------------------------------------
# Noticias
# ---------------------------------------------------------------------
@inicio_bp.route("/noticias")
def noticias():
    """Listado completo de noticias, ordenadas por fecha descendente."""
    noticias = Noticia.query.order_by(Noticia.fecha.desc()).all()
    return render_template("inicio/noticias.html", noticias=noticias)


@inicio_bp.route("/noticia/<int:id>")
def ver_noticia(id):
    """Detalle de una noticia específica."""
    noticia = Noticia.query.get_or_404(id)
    return render_template("inicio/ver_noticia.html", noticia=noticia)


# ---------------------------------------------------------------------
# Avisos
# ---------------------------------------------------------------------
@inicio_bp.route("/avisos")
def avisos():
    """Lista solo los avisos activos (vigentes)."""
    hoy = date.today()
    avisos = (
        Aviso.query
        .filter(Aviso.fecha_inicio <= hoy)
        .filter((Aviso.fecha_fin == None) | (Aviso.fecha_fin >= hoy))
        .order_by(Aviso.fecha_inicio.desc())
        .all()
    )
    return render_template("inicio/avisos.html", avisos=avisos)


# ---------------------------------------------------------------------
# Eventos
# ---------------------------------------------------------------------
@inicio_bp.route("/eventos")
def eventos():
    """Listado completo de eventos futuros y recientes."""
    eventos = Evento.query.order_by(Evento.fecha.desc()).all()
    return render_template("inicio/eventos.html", eventos=eventos)
