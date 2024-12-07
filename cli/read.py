from cli import cli
from data import Library


@cli.command()
def read():
    library = Library()
    print(library)



