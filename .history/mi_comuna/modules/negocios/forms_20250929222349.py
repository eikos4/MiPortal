from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileField, FileAllowed

class NegocioForm(FlaskForm):
    nombre = StringField(
        "Nombre del Negocio",
        validators=[DataRequired(), Length(min=2, max=150)]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[Optional(), Length(max=500)]
    )
    direccion = StringField(
        "Dirección",
        validators=[DataRequired(), Length(max=200)]
    )
    telefono = StringField(
        "Teléfono",
        validators=[Optional(), Length(max=20)]
    )
    whatsapp = StringField(
        "WhatsApp",
        validators=[Optional(), Length(max=20)]
    )
    horario = StringField(
        "Horario de Atención",
        validators=[Optional(), Length(max=100)]
    )
    redes = StringField(
        "Redes Sociales (ej. @instagram, @facebook)",
        validators=[Optional(), Length(max=150)]
    )
    categoria_id = SelectField(
        "Categoría",
        coerce=int,
        validators=[DataRequired()]
    )

    # Imagen o logo del negocio
    imagen = FileField(
        "Imagen o Logo",
        validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "gif"], "Solo se permiten imágenes")]
    )

    submit = SubmitField("Registrar Negocio")
