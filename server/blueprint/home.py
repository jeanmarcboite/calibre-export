import json

from flask import Blueprint, render_template

from data import Book, library

name = "home"

bp = Blueprint(name.capitalize(), __name__, url_prefix=f'/')

@bp.route("/")
def index():
    return render_template(
            f'pages/{name}.html',
        header=Book.columns(),
        books = library.books
    )


@bp.route('/api/data')
def data():
    return list(map(lambda book: book.to_dict(), library.books.values())), 200
