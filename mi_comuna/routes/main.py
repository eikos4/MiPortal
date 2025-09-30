# app/routes/main.py
from flask import Blueprint, render_template

main = Blueprint('main', __name__)



from flask import current_app

@main.app_context_processor
def inject_current_app():
    return dict(current_app=current_app)

@main.route('/')
def index():
    return render_template("index.html")
