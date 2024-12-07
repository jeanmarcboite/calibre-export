
from cli import cli
from server import run

@cli.command()
def server():
    run(True)

