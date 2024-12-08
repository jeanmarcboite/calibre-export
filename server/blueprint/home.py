from flask import Blueprint, render_template

from data import Book, library

name = "home"

bp = Blueprint(name.capitalize(), __name__, url_prefix=f'/{name}/')

@bp.route("/")
def index():
    return render_template(
            f'pages/{name}.html',
        data=list(map(lambda col: col.to_dict(), library.books.values())),
        header=Book.columns(),
        books = library.books
    )