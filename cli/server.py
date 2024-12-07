
from cli import cli
from data import Library
from server import run

@cli.command()
def server():
    library = Library()
    #print(library)
    run(True)

