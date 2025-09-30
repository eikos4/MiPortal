from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileField, FileAllowed

class NegocioForm(FlaskForm):
    nombre = StringField("Nombre del Negocio", validators=[DataRequired(), Length(min=2, max=150)])
    descripcion = TextAreaField("Descripción", validators=[Length(max=500)])
    direccion = StringField("Dirección", validators=[DataRequired(), Length(max=200)])
    telefono = StringField("Teléfono", validators=[Optional(), Length(max=20)])
    whatsapp = StringField("WhatsApp", validators=[Optional(), Length(max=20)])
    horario = StringField("Horario de Atención", validators=[Optional(), Length(max=100)])
    redes = StringField("Redes Sociales (ej. @instagram, @facebook)", validators=[Optional(), Length(max=150)])
    categoria_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])

    # Campo para subir imagen/logo
    imagen = FileField("Imagen o Logo", validators=[
        Optional(),
        FileAllowed(["jpg", "jpeg", "png", "gif"], "Solo se permiten imágenes")
    ])

    submit = SubmitField("Registrar Negocio")
# mi_comuna/modules/ciudadano/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional

class PerfilEmpresaForm(FlaskForm):
    nombre = StringField("Nombre de la empresa", validators=[DataRequired()])
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    direccion = StringField("Dirección", validators=[Optional()])
    telefono = StringField("Teléfono", validators=[Optional()])
    whatsapp = StringField("WhatsApp", validators=[Optional()])
    email = StringField("Correo electrónico", validators=[Optional()])
    sitio_web = StringField("Sitio web", validators=[Optional()])
    facebook = StringField("Facebook", validators=[Optional()])
    instagram = StringField("Instagram", validators=[Optional()])
    tiktok = StringField("TikTok", validators=[Optional()])
    horario = StringField("Horario de atención", validators=[Optional()])
    categoria_id = StringField("Categoría", validators=[Optional()])  # si usas SelectField mejor

    # 👇 este es el nuevo
    logo = FileField("Logo (opcional)")

    submit = SubmitField("Guardar cambios")
