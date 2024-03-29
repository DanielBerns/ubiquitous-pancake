from pathlib import Path

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    root = Path('~', '.flaskr').expanduser()
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    app = Flask(__name__, 
                instance_path=str(root), 
                instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=Path(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return "<p>Hello, World!</p>"

    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
