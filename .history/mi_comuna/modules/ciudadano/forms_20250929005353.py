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
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional

class PerfilEmpresaForm(FlaskForm):
    nombre = StringField("Nombre de la empresa", validators=[DataRequired()])
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    direccion = StringField("Dirección", validators=[Optional()])
    telefono = StringField("Teléfono", validators=[Optional()])
    whatsapp = StringField("WhatsApp", validators=[Optional()])  # 👈 agregado
    redes = StringField("Redes Sociales", validators=[Optional()])
    submit = SubmitField("Guardar cambios")



# mi_comuna/modules/ciudadano/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Optional

class NoticiaForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    contenido = TextAreaField("Contenido", validators=[DataRequired()])
    imagen = FileField("Imagen", validators=[Optional()])
    submit = SubmitField("Publicar Noticia")

class EventoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    fecha = DateField("Fecha", validators=[DataRequired()])
    lugar = StringField("Lugar", validators=[Optional()])
    imagen = FileField("Imagen", validators=[Optional()])
    submit = SubmitField("Publicar Evento")
