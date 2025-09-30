from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired

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


#