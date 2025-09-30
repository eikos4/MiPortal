from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired

class NoticiaForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    contenido = TextAreaField("Contenido", validators=[DataRequired()])
    fecha = DateField("Fecha", validators=[DataRequired()])
    submit = SubmitField("Guardar")

# mi_comuna/modules/inicio/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class AvisoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    imagen = FileField("Imagen", validators=[Optional()])
    submit = SubmitField("Publicar Aviso")


