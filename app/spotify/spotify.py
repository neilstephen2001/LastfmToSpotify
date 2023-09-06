import base64

from flask import Blueprint, redirect, url_for, request, render_template, session
from requests import HTTPError

from app.spotify.services import generate_playlist, return_playlist, AuthenticationError

spotify_blueprint = Blueprint('spotify_bp', __name__)


@spotify_blueprint.route('/create-playlist', methods=['POST'])
def create_playlist():
    if 'export' in request.form:
        return render_template('create-playlist.html')
    else:
        return redirect(url_for('home_bp.home'))


@spotify_blueprint.route('/display-playlist', methods=['POST'])
def display_playlist():
    try:
        name = request.form.get('playlist-name')
        description = request.form.get('description')
        public = False

        cover_art = request.files['cover-art']
        encoded_image = base64.b64encode(cover_art.read())

        generate_playlist(name, description, public, encoded_image)
        playlist = return_playlist()
        print(return_playlist())
        return render_template('display-playlist.html', value=playlist['embedded_url'])

    except AuthenticationError:
        # Spotify authentication expired, need to log in again
        return redirect(url_for('auth_bp.login'))

    except HTTPError:
        return redirect(url_for('home_bp.error'))

