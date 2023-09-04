import base64
import json

from flask import Blueprint, redirect, url_for, request, render_template

from app.spotify import services

spotify_blueprint = Blueprint('spotify_bp', __name__)


@spotify_blueprint.route('/export-playlist', methods=['POST'])
def export_playlist():
    if 'export' in request.form:
        return render_template('create-playlist.html')
    else:
        return redirect(url_for('index'))


@spotify_blueprint.route('/playlist-create', methods=['POST'])
def playlist_create():
    playlist_details = json.dumps({
        'name': request.form.get('playlist-name'),
        'description': request.form.get('description'),
        'public': False
    })
    song_uri = []
    cover_art = request.files['cover-art']
    encoded_image = base64.b64encode(cover_art.read())
    embedded_playlist_url = services.create_playlist(playlist_details, song_uri, encoded_image)
    return redirect(url_for('playlist_display'))


@spotify_blueprint.route('/playlist_display')
def playlist_display():
    """return render_template('display-playlist.html', value = embedded_playlist_url)"""
