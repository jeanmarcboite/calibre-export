from flask import current_app

from server.blueprint import home


def register_blueprints(flask_app):
    flask_app.register_blueprint(home.bp)
    ctx = flask_app.app_context()
    ctx.push()
    left = [('/', 'Dashboard')]
    links = []
    current_app.config['links'] = left + list(map(lambda x: (x.bp.url_prefix, x.bp.name), links))
    print (current_app.config['links'])
    ctx.pop()
    for link in links:
        flask_app.register_blueprint(link.bp)
