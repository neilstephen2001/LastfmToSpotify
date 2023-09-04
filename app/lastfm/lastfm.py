from flask import Blueprint, redirect, url_for, jsonify, request

from app.lastfm.services import get_album_image, get_top_tracks
from app.spotify.services import get_song_uri

lastfm_blueprint = Blueprint('lastfm_bp', __name__)


@lastfm_blueprint.route('/submit-lastfm', methods=['POST'])
def submit_lastfm():
    username = request.form['username']
    time_period = request.form['time-period']
    tracks = request.form['tracks']
    return redirect(url_for('get_data'))


@lastfm_blueprint.route('/get-data')
def get_data():
    """track_data = get_top_tracks(user = username, period = time_period, limit = tracks)
    song_uri, album_list = get_song_uri(track_data)
    get_album_image(album_list, track_data)
    return redirect(url_for('results'))"""


@lastfm_blueprint.route('/process-data')
def process_data():
    """return jsonify(track_data)"""


@lastfm_blueprint.route('/results')
def results():
    """if time_period == '7day':
        period = 'last 7 days'
    elif time_period == '1month':
        period = 'last 30 days'
    elif time_period == '3month':
        period = 'last 90 days'
    elif time_period == '6month':
        period = 'last 180 days'
    elif time_period == '12month':
        period = 'last 365 days'
    else:
        period = 'all-time'
    return render_template('display-results.html', username = username, tracks = tracks, period = period)"""