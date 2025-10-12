from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Optional

class NegocioForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField("Descripción", validators=[Optional(), Length(max=1000)])
    direccion = StringField("Dirección", validators=[DataRequired(), Length(max=200)])
    telefono = StringField("Teléfono", validators=[Optional(), Length(max=50)])
    whatsapp = StringField("WhatsApp", validators=[Optional(), Length(max=50)])
    redes = StringField("Redes Sociales", validators=[Optional(), Length(max=200)])
    horarios = StringField("Horarios", validators=[Optional(), Length(max=200)])
    categoria_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    imagen = FileField("Imagen (opcional)")
