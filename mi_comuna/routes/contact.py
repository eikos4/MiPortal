from flask import Blueprint, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

bp = Blueprint('contact', __name__, url_prefix='/contact')

class ContactForm(FlaskForm):
    nombre = StringField("Tu nombre", validators=[DataRequired()])
    email = StringField("Tu correo", validators=[DataRequired(), Email()])
    mensaje = TextAreaField("Mensaje", validators=[DataRequired()])
    submit = SubmitField("Enviar")

@bp.route('/', methods=['GET', 'POST'])
def form():
    form = ContactForm()
    if form.validate_on_submit():
        flash("Mensaje enviado correctamente (ficticio)", "success")
        return redirect(url_for("main.index"))
    return render_template('contact/form.html', form=form)
