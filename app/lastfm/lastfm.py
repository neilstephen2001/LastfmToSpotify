from flask import Blueprint, request, render_template, url_for, redirect
from requests import HTTPError

from app.lastfm.services import request_top_tracks, return_top_tracks
from app.lastfm.utilities import process_time_period
import app.adapters.repository as repo
from app.spotify.services import AuthenticationError

lastfm_blueprint = Blueprint('lastfm_bp', __name__)


@lastfm_blueprint.route('/top-tracks', methods=['POST'])
def display_results():
    try:
        lastfm_user = request.form['user']
        period = request.form['time-period']
        track_count = int(request.form['track-count'])
        request_top_tracks(lastfm_user, period, track_count, repo.repo_instance)
        return render_template('display-results.html',
                               user=lastfm_user,
                               period=process_time_period(period),
                               track_count=track_count,
                               songs=return_top_tracks(repo.repo_instance))

    except ValueError:
        # Invalid parameters, need to re-enter
        return redirect(url_for('home_bp.home'))

    except AuthenticationError:
        # Spotify authentication expired, need to log in again
        return redirect(url_for('auth_bp.login'))

    except HTTPError:
        return redirect(url_for('home_bp.error'))
