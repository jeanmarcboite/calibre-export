import click

from app import set_logger
from app.calibre_library import CalibreLibrary


@click.group()
@click.option('--library', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True))
@click.option('-o', '--output', type=click.Path(file_okay=False, dir_okay=True, readable=True, writable=True))
@click.option('--debug/--no-debug', default=False,
              envvar='PYTHON_DEBUG')
@click.pass_context
def cli(ctx, library, output, debug):
    set_logger()
    ctx.obj = CalibreLibrary(library, output, debug)

