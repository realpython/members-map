import os
from flask import Flask
import map
import db_pg


def create_app(test_config=None):
    # create and cofigure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'here will come the map later'

    app.register_blueprint(map.bp)
    app.add_url_rule('/', endpoint='index')

    db_pg.init_app(app)

    return app

app = create_app()
if __name__ == '__main__':
    app.run()