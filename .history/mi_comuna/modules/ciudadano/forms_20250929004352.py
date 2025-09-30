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
        validators=[DataRequired(message="El nombre es obligatorio")]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[Optional()]
    )
    direccion = StringField(
        "Dirección",
        validators=[Optional()]
    )
    telefono = StringField(
        "Teléfono",
        validators=[Optional()]
    )
    redes = StringField(
        "Redes Sociales",
        validators=[Optional()]
    )
    submit = SubmitField("Guardar cambios")
