# mi_comuna/modules/ciudadano/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


# -----------------------
# Formulario de Noticias
# -----------------------
class NoticiaForm(FlaskForm):
    titulo = StringField(
        "📰 Título",
        validators=[
            DataRequired(message="⚠️ El título es obligatorio"),
            Length(max=200, message="Máximo 200 caracteres")
        ]
    )
    contenido = TextAreaField(
        "📝 Contenido",
        validators=[DataRequired(message="⚠️ El contenido es obligatorio")]
    )
    imagen = FileField("🖼 Imagen (opcional)")
    fecha_publicacion = DateField(
        "📅 Fecha de publicación",
        format="%Y-%m-%d",
        validators=[Optional()]
    )
    submit = SubmitField("💾 Publicar Noticia")


# -----------------------
# Formulario de Eventos
# -----------------------
class EventoForm(FlaskForm):
    titulo = StringField(
        "🎉 Título del evento",
        validators=[
            DataRequired(message="⚠️ El título es obligatorio"),
            Length(max=200, message="Máximo 200 caracteres")
        ]
    )
    descripcion = TextAreaField(
        "📝 Descripción",
        validators=[DataRequired(message="⚠️ La descripción es obligatoria")]
    )
    fecha_inicio = DateField(
        "📅 Fecha de inicio",
        format="%Y-%m-%d",
        validators=[DataRequired(message="⚠️ La fecha de inicio es obligatoria")]
    )
    fecha_fin = DateField(
        "📅 Fecha de fin",
        format="%Y-%m-%d",
        validators=[Optional()]
    )
    lugar = StringField(
        "📍 Lugar",
        validators=[Optional(), Length(max=255)]
    )
    imagen = FileField("🖼 Imagen (opcional)")
    submit = SubmitField("💾 Publicar Evento")
