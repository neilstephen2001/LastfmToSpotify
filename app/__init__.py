from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    with app.app_context():
        from .auth import auth
        app.register_blueprint(auth.auth_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .lastfm import lastfm
        app.register_blueprint(lastfm.lastfm_blueprint)

        from .spotify import spotify
        app.register_blueprint(spotify.spotify_blueprint)

        return app
