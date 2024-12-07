from flask import Blueprint, render_template

from calibre_db import CustomColumns
from data import Book, library

name = "custom_columns"

bp = Blueprint(name.capitalize(), __name__, url_prefix=f'/{name}/')

@bp.route('/api/data')
def data():
    custom_columns = []
    for col in library.calibre.custom_column.values():
        custom_columns.append(col.pretty_row())
    print(custom_columns)

    return {'data': custom_columns}

@bp.route("/")
def index():
    rows = []
    for col in library.calibre.custom_column.values():
        rows.append(col.pretty_row())

    return render_template(
            f'pages/{name}.html',
        header= CustomColumns.pretty_header(),
        columns=["Label", "Name", "Datatype", "delete", "edit", "display", "mult", "norm"],
        custom_columns = rows
    )