from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired

class NoticiaForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    contenido = TextAreaField("Contenido", validators=[DataRequired()])
    fecha = DateField("Fecha", validators=[DataRequired()])
    submit = SubmitField("Guardar")

class AvisoForm(FlaskForm):
    mensaje = StringField("Mensaje", validators=[DataRequired()])
    fecha_inicio = DateField("Inicio", validators=[DataRequired()])
    fecha_fin = DateField("Fin")
    submit = SubmitField("Guardar")

class EventoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    lugar = StringField("Lugar", validators=[DataRequired()])
    fecha = DateField("Fecha", validators=[DataRequired()])
    hora = TimeField("Hora")
    descripcion = TextAreaField("Descripción")
    submit = SubmitField("Guardar")
