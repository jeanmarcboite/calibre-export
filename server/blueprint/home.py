from flask import Blueprint, render_template

from data import Book

name = "home"

bp = Blueprint(name.capitalize(), __name__, url_prefix=f'/{name}/')

@bp.route("/")
def index():
    return render_template(
            f'pages/{name}.html', header=Book.header())