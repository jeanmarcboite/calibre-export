from cli import cli
from data import library


@cli.command()
def read():
    print(library)



