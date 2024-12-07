import click
from flask import Flask, render_template, jsonify
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

from data import Book, Library
from server.blueprint import register_blueprints


# Function that create the app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # Simple route
    @app.route('/')
    def index():
        library = Library()
        #print(library.books)
        return render_template(
            f'pages/home.html',
            header=Book.header(),
            books=library.books
        )

    @app.route('/hello')
    def hello_world():
        return jsonify({
            "status": "success",
            "message": "Hello World!"
        })

    return app  # do not forget to return the app


def run(debug: bool):
    flask_app = create_app()
    flask_app.jinja_env.undefined = StrictUndefined
    register_blueprints(flask_app)
    # set a 'SECRET_KEY' to enable the Flask session cookies
    flask_app.debug = True
    flask_app.config['SECRET_KEY'] = '<replace with a secret key>'
    debugtoolbar = DebugToolbarExtension(flask_app)
    flask_app.run(debug=debug)

