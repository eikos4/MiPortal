# mi_comuna/modules/ciudadano/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


# -----------------------
# Formulario de Ofertas
# -----------------------
class OfertaForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="El título es obligatorio"), Length(max=150)]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="La descripción es obligatoria")]
    )
    imagen = FileField("Imagen (opcional)")
    fecha_inicio = DateField(
        "Fecha inicio",
        format="%Y-%m-%d",
        validators=[Optional()]
    )
    fecha_fin = DateField(
        "Fecha fin",
        format="%Y-%m-%d",
        validators=[Optional()]
    )
    submit = SubmitField("Guardar Oferta")


# -----------------------
# Formulario de Perfil Empresa
# -----------------------
class PerfilEmpresaForm(FlaskForm):
    nombre = StringField(
        "Nombre de la empresa",
        validators=[DataRequired(message="El nombre de la empresa es obligatorio")]
    )
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    direccion = StringField("Dirección", validators=[Optional()])
    telefono = StringField("Teléfono", validators=[Optional()])
    whatsapp = StringField("WhatsApp", validators=[Optional()])
    redes = StringField("Redes Sociales", validators=[Optional()])
    submit = SubmitField("Guardar cambios")


# -----------------------
# Formulario de Avisos
# -----------------------
class AvisoForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="El título es obligatorio"), Length(max=150)]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="La descripción es obligatoria")]
    )
    imagen = FileField("Imagen (opcional)")
    submit = SubmitField("Publicar Aviso")


# -----------------------
# Formulario de Noticias
# -----------------------
class NoticiaForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="El título es obligatorio"), Length(max=200)]
    )
    contenido = TextAreaField(
        "Contenido",
        validators=[DataRequired(message="El contenido es obligatorio")]
    )
    imagen = FileField("Imagen (opcional)")
    fecha_publicacion = DateField(
        "Fecha publicación",
        format="%Y-%m-%d",
        validators=[Optional()]
    )
    submit = SubmitField("Publicar Noticia")


# -----------------------
# Formulario de Eventos
# -----------------------
class EventoForm(FlaskForm):
    titulo = StringField(
        "Título del evento",
        validators=[DataRequired(message="El título del evento es obligatorio"), Length(max=200)]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="La descripción es obligatoria")]
    )
    fecha_inicio = DateField(
        "Fecha inicio",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La fecha de inicio es obligatoria")]
    )
    fecha_fin = DateField(
        "Fecha fin",
        format="%Y-%m-%d",
        validators=[Optional()]
    )
    lugar = StringField("Lugar", validators=[Optional(), Length(max=255)])
    imagen = FileField("Imagen (opcional)")
    submit = SubmitField("Publicar Evento")
