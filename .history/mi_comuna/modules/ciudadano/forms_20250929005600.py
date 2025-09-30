from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp


# -----------------------
# Formulario de Ofertas
# -----------------------
class OfertaForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[
            DataRequired(message="⚠️ El título es obligatorio"),
            Length(max=150, message="⚠️ Máximo 150 caracteres")
        ]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="⚠️ La descripción es obligatoria")]
    )
    imagen = FileField("🖼 Imagen (opcional)")
    fecha_inicio = DateField(
        "📅 Fecha inicio",
        format="%Y-%m-%d",
        validators=[Optional()],
        description="Formato: AAAA-MM-DD"
    )
    fecha_fin = DateField(
        "📅 Fecha fin",
        format="%Y-%m-%d",
        validators=[Optional()],
        description="Formato: AAAA-MM-DD"
    )
    submit = SubmitField("💾 Guardar Oferta")


# -----------------------
# Formulario de Perfil Empresa
# -----------------------
class PerfilEmpresaForm(FlaskForm):
    nombre = StringField(
        "🏢 Nombre de la empresa",
        validators=[DataRequired(message="⚠️ El nombre es obligatorio")]
    )
    descripcion = TextAreaField(
        "📝 Descripción",
        validators=[Optional()]
    )
    direccion = StringField(
        "📍 Dirección",
        validators=[Optional()]
    )
    telefono = StringField(
        "📞 Teléfono",
        validators=[
            Optional(),
            Regexp(r"^\+?[0-9\s\-]{7,20}$", message="⚠️ Ingresa un teléfono válido")
        ]
    )
    whatsapp = StringField(
        "💬 WhatsApp",
        validators=[
            Optional(),
            Regexp(r"^\+?[0-9\s\-]{7,20}$", message="⚠️ Ingresa un número válido de WhatsApp")
        ]
    )
    redes = StringField(
        "🌐 Redes Sociales",
        validators=[Optional()],
        description="Ejemplo: https://instagram.com/miempresa"
    )
    submit = SubmitField("💾 Guardar cambios")
