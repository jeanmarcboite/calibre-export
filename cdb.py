import os

import click
# python $exe authors --library $library  -o $output/authors


class CalibreLibrary(object):
    def __init__(self, library=None, debug=False):
        self.calibre_library = os.path.abspath(library or '.')
        self.debug = debug


@click.group()
@click.option('--library', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True))
@click.option('--debug/--no-debug', default=False,
              envvar='PYTHON_DEBUG')
@click.pass_context
def cli(ctx, library, debug):
    ctx.obj = CalibreLibrary(library, debug)

@cli.command()
@click.option('-f', '--fmt', '--format', '--file-type', default='all', type=str)
@click.argument('output')
@click.pass_obj
def authors(o, output, fmt):
    click.echo(f'authors {o.calibre_library} {output} {fmt}')

if __name__ == '__main__':
    cli(auto_envvar_prefix='CALIBRE')