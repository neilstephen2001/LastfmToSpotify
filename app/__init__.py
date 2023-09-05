import os
import app.adapters.repository as repo

from flask import Flask
from app.adapters.memory_repository import MemoryRepository


def create_app():

    # Create flask app object, configure application and load in secret keys
    app = Flask(__name__, static_folder=os.getcwd()+"\\static")
    app.config.from_pyfile('config.py')
    app.template_folder = os.getcwd() + "\\templates"

    repo.repo_instance = MemoryRepository()

    # Register blueprints
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
