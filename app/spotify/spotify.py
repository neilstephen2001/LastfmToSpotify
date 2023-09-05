import base64
import json

from flask import Blueprint, redirect, url_for, request, render_template
import app.adapters.repository as repo
from app.spotify.services import generate_playlist

spotify_blueprint = Blueprint('spotify_bp', __name__)


@spotify_blueprint.route('/create-playlist', methods=['POST'])
def create_playlist():
    if 'export' in request.form:
        return render_template('create-playlist.html')
    else:
        return redirect(url_for('home_bp.home'))


@spotify_blueprint.route('/display-playlist')
def display_playlist():
    playlist_details = json.dumps({
        'name': request.form.get('playlist-name'),
        'description': request.form.get('description'),
        'public': False
    })
    cover_art = request.files['cover-art']
    encoded_image = base64.b64encode(cover_art.read())
    print(playlist_details)
    embedded_playlist_url = generate_playlist(repo.repo_instance, playlist_details, encoded_image)
    return render_template('display-playlist.html', value=embedded_playlist_url)
