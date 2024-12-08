from re import sub

from flask import Blueprint, render_template

from calibre_db import *
from data import Book, library

name = "custom_columns"

bp = Blueprint(sub(r"(_|-)+", " ", name).title().replace(" ", ""), __name__, url_prefix=f'/{name}/')

@bp.route('/api/data')
def data():
    return list(map(lambda column: column.to_dict(), library.calibre.custom_column.values())), 200

@bp.route("/")
def index():
    print (dir(bp))
    return render_template(
            f'pages/{name}.html',
        ajaxURL = f'/{name}/api/data',
        header=CustomColumns.columns()
    )
