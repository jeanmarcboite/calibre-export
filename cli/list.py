import click
from texttable import Texttable

from app import logger
from calibre_db import CustomColumns
from cli import cli
from data import library


@cli.command()
@click.option('-l', '--label', type=str)
@click.option('-v', '--value', type=str)
def list_column():
    pass

@cli.command()
def list_columns():
    print(library.calibre.custom_column)
    table = Texttable()
    table.header(CustomColumns.pretty_header())
    table.set_cols_width(CustomColumns.cols_width())
    for col in library.calibre.custom_column.values():
        table.add_row(col.pretty_row())
    print(table.draw())


@cli.command()
@click.option('-t', '--table', type=str)
@click.option('-f', '--field', type=str, default='name')
def list(table, field='name'):
    try:
        table_class = globals()[table]
        query = table_class.select()
        print(query.sql())
        for entry in query:
            print(getattr(entry, field))
    except KeyError:
        logger.error(f'No such table {table}')
    except Exception as e:
        logger.error(repr(e))

