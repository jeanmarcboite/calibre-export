import os
import logging
from email.policy import default

import click
# python $exe authors --library $library  -o $output/authors
from calibre_db import db
from calibre_db.base_model import sqlite_db
from calibre_db.metadata import get_authors
from data import Library

logger = logging.getLogger(__name__)

class CalibreLibrary(object):
    def __init__(self, library=None, output=None, debug=False):
        self.calibre_library = os.path.abspath(library or '.')
        self.output = os.path.abspath(output or '.')
        self.debug = debug
        database = os.path.join(self.calibre_library, 'metadata.db')
        # Check if db already exists or not
        if not os.path.exists(database):
            raise ValueError(f'DB {database} does not exist')
        sqlite_db.init(database)
@click.group()
@click.option('--library', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True))
@click.option('-o', '--output', type=click.Path(file_okay=False, dir_okay=True, readable=True, writable=True))
@click.option('--debug/--no-debug', default=False,
              envvar='PYTHON_DEBUG')
@click.pass_context
def cli(ctx, library, output, debug):
    click.echo(f'open {library}')
    ctx.obj = CalibreLibrary(library, output, debug)

@cli.command()
@click.option('-f', '--fmt', '--format', '--file-type', default='all', type=str)
@click.pass_obj
def authors(o, fmt):
    click.echo(f'authors {o.calibre_library} {o.output} {fmt}')
    authors = get_authors()
    print(authors)

def list_table(table_class, field):
    query = table_class.select()
    print(query.sql())
    for entry in query:
        print(getattr(entry, field))

@cli.command()
@click.option('-t', '--table', type = str)
@click.option('-f', '--field', type = str, default = 'name')
def list(table, field = 'name'):
    cls = globals()[table]
    list_table(cls, field)

@cli.command()
def read():
    library = Library()
    print(library)



def set_logger():
    logger.setLevel(logging.ERROR)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

if __name__ == '__main__':
    set_logger()
    if True:
        click.echo('run cli')
        cli(auto_envvar_prefix='CALIBRE')
    else:
        try:
            cli(auto_envvar_prefix='CALIBRE')
        except Exception as error:
            logger.error(repr(error))