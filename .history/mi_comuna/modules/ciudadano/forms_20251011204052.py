# mi_comuna/modules/ciudadano/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email


# ======================================================
# 💰 Formulario de Ofertas
# ======================================================
class OfertaForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[
            DataRequired(message="El título es obligatorio."),
            Length(max=150, message="Máximo 150 caracteres.")
        ]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="La descripción es obligatoria.")]
    )
    imagen = FileField(
        "Imagen (opcional)",
        validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "webp", "gif"], "Solo se permiten imágenes.")]
    )
    fecha_inicio = DateField("Fecha de inicio", format="%Y-%m-%d", validators=[Optional()])
    fecha_fin = DateField("Fecha de término", format="%Y-%m-%d", validators=[Optional()])
    submit = SubmitField("Guardar Oferta")


# ======================================================
# 🏢 Formulario de Perfil Empresa
# ======================================================
class PerfilEmpresaForm(FlaskForm):
    nombre = StringField(
        "Nombre de la empresa",
        validators=[DataRequired(message="El nombre es obligatorio."), Length(max=120)]
    )
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    direccion = StringField("Dirección", validators=[Optional(), Length(max=255)])
    telefono = StringField("Teléfono", validators=[Optional(), Length(max=50)])
    whatsapp = StringField("WhatsApp", validators=[Optional(), Length(max=50)])
    email = StringField("Correo electrónico", validators=[Optional(), Email(message="Correo inválido.")])
    sitio_web = StringField("Sitio web", validators=[Optional(), Length(max=255)])
    facebook = StringField("Facebook", validators=[Optional(), Length(max=255)])
    instagram = StringField("Instagram", validators=[Optional(), Length(max=255)])
    tiktok = StringField("TikTok", validators=[Optional(), Length(max=255)])
    horario = StringField("Horario de atención", validators=[Optional(), Length(max=255)])

    categoria_id = SelectField(
        "Categoría",
        coerce=int,
        validators=[Optional()],
        choices=[]  # Se carga dinámicamente en la vista
    )

    logo = FileField(
        "Logo (opcional)",
        validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "webp", "gif"], "Solo se permiten imágenes.")]
    )

    submit = SubmitField("Guardar cambios")


# ======================================================
# 📢 Formulario de Avisos
# ======================================================
class AvisoForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[
            DataRequired(message="El título es obligatorio."),
            Length(max=150, message="Máximo 150 caracteres.")
        ]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="La descripción es obligatoria.")]
    )
    imagen = FileField(
        "Imagen (opcional)",
        validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "webp", "gif"], "Solo se permiten imágenes.")]
    )
    submit = SubmitField("Publicar Aviso")


# ======================================================
# 📰 Formulario de Noticias
# ======================================================

class NoticiaForm(FlaskForm):
    """
    📰 Formulario para crear o editar noticias de empresas ciudadanas.
    Incluye validaciones completas y soporte para imagen opcional.
    """

    # 🔹 Campo título
    titulo = StringField(
        label="Título de la noticia",
        validators=[
            DataRequired(message="El título es obligatorio."),
            Length(max=200, message="El título no puede superar los 200 caracteres."),
        ],
        render_kw={
            "placeholder": "Ejemplo: Nueva sucursal en el centro de Parral",
            "class": "w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-blue-500"
        }
    )

    # 🔹 Contenido
    contenido = TextAreaField(
        label="Contenido de la noticia",
        validators=[
            DataRequired(message="El contenido no puede estar vacío."),
            Length(min=20, message="Debe contener al menos 20 caracteres."),
        ],
        render_kw={
            "rows": 6,
            "placeholder": "Describe los detalles de la noticia...",
            "class": "w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-blue-500"
        }
    )

    # 🔹 Imagen (opcional)
    imagen = FileField(
        label="Imagen ilustrativa (opcional)",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png", "webp", "gif"], "Solo se permiten imágenes (JPG, PNG, WEBP, GIF).")
        ],
        render_kw={
            "class": (
                "block w-full text-sm text-gray-600 "
                "file:mr-4 file:py-2 file:px-4 "
                "file:rounded-lg file:border-0 "
                "file:text-sm file:font-semibold "
                "file:bg-blue-600 file:text-white "
                "hover:file:bg-blue-700 cursor-pointer"
            )
        }
    )

    # 🔹 Botón enviar
    submit = SubmitField(
        "📰 Publicar Noticia",
        render_kw={
            "class": (
                "px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white "
                "font-semibold rounded-lg shadow transition w-full sm:w-auto"
            )
        }
    )


# ======================================================
# 🎉 Formulario de Eventos
# ======================================================
class EventoForm(FlaskForm):
    titulo = StringField(
        "Título del evento",
        validators=[
            DataRequired(message="El título del evento es obligatorio."),
            Length(max=200, message="Máximo 200 caracteres.")
        ]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired(message="La descripción es obligatoria.")]
    )
    fecha_inicio = DateField(
        "Fecha de inicio",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La fecha de inicio es obligatoria.")]
    )
    fecha_fin = DateField("Fecha de término", format="%Y-%m-%d", validators=[Optional()])
    lugar = StringField("Lugar", validators=[Optional(), Length(max=255)])
    imagen = FileField(
        "Imagen (opcional)",
        validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "webp", "gif"], "Solo se permiten imágenes.")]
    )
    submit = SubmitField("Publicar Evento")
