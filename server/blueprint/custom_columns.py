from flask import Blueprint, render_template

from calibre_db import *
from data import Book, library

name = "custom_columns"

bp = Blueprint(name.capitalize(), __name__, url_prefix=f'/{name}/')

@bp.route('/api/data')
def data():

    custom_columns = []
    for custom_column in library.calibre.custom_column.values():
        custom_columns.append(custom_column.to_list())
    print(custom_columns)

    return {'data': custom_columns}

@bp.route("/")
def index():
    rows = []
    for custom_column in library.calibre.custom_column.values():
        rows.append(custom_column.to_list())

    return render_template(
            f'pages/{name}.html',
        header= CustomColumns.header(),
        custom_columns = rows
    )