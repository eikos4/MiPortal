from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

class OfertaForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    imagen = FileField("Imagen")
    fecha_inicio = DateField("Fecha inicio", format="%Y-%m-%d")
    fecha_fin = DateField("Fecha fin", format="%Y-%m-%d")
    submit = SubmitField("Guardar Oferta")
