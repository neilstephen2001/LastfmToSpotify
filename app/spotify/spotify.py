import base64

from flask import Blueprint, redirect, url_for, request, render_template, session
from requests import HTTPError

from app.spotify.services import generate_playlist, return_playlist, AuthenticationError

spotify_blueprint = Blueprint('spotify_bp', __name__)


@spotify_blueprint.route('/create-playlist', methods=['GET', 'POST'])
def create_playlist():
    error_message = session.pop('playlist_form_error', None)
    if 'home' in request.form:
        return redirect(url_for('home_bp.home'))
    else:
        return render_template('create-playlist.html', error_message=error_message)


@spotify_blueprint.route('/display-playlist', methods=['POST'])
def display_playlist():
    try:
        # Playlist name is required
        name = request.form.get('playlist-name')
        if name == "":
            raise ValueError('playlist-name')
        description = request.form.get('description')
        public = False

        # Validate that image to be uploaded is less than 256 kB
        cover_art = request.files['cover-art']
        if cover_art and len(cover_art.read()) > 256 * 1024:
            raise ValueError('cover-art')

        generate_playlist(name, description, public, base64.b64encode(cover_art.read()))
        playlist = return_playlist()
        return render_template('display-playlist.html', value=playlist['embedded_url'])

    except ValueError as e:
        if str(e) == 'playlist-name':
            session['playlist_form_error'] = 'Playlist name is required.'
        else:
            session['playlist_form_error'] = 'File size is too large.'
        return redirect(url_for('spotify_bp.create_playlist'))

    except AuthenticationError:
        # Spotify authentication expired, need to log in again
        return redirect(url_for('auth_bp.login'))

    except HTTPError:
        return redirect(url_for('home_bp.error'))

