import base64
import json

from flask import Blueprint, redirect, url_for, request, render_template
from requests import HTTPError

import app.adapters.repository as repo
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
        playlist_details = json.dumps({
            'name': request.form.get('playlist-name'),
            'description': request.form.get('description'),
            'public': False
        })
        cover_art = request.files['cover-art']
        encoded_image = base64.b64encode(cover_art.read())
        print(playlist_details)
        generate_playlist(repo.repo_instance, playlist_details, encoded_image)
        playlist = return_playlist(repo.repo_instance)
        return render_template('display-playlist.html', value=playlist.embedded_url)

    except AuthenticationError:
        # Spotify authentication expired, need to log in again
        return redirect(url_for('auth_bp.login'))

    except HTTPError:
        return redirect(url_for('home_bp.error'))

