from flask import Blueprint, render_template

from calibre_db import *
from data import Book, library

name = "custom_columns"

bp = Blueprint(name.capitalize(), __name__, url_prefix=f'/{name}/')

@bp.route('/api/data')
def data():
    custom_columns = list(map(lambda custom_col: custom_col.to_list(), library.calibre.custom_column.values()))
    return {'data': custom_columns}

@bp.route("/")
def index():
    return render_template(
            f'pages/{name}.html',
        data=list(map(lambda custom_col: custom_col.to_dict(), library.calibre.custom_column.values())),
        header= CustomColumns.columns(),
    )