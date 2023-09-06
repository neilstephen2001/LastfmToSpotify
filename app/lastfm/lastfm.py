from flask import Blueprint, request, render_template, url_for, redirect, session
from requests import HTTPError

from app.lastfm.services import request_top_tracks, return_top_tracks
from app.lastfm.utilities import process_time_period
from app.spotify.services import AuthenticationError

lastfm_blueprint = Blueprint('lastfm_bp', __name__)


@lastfm_blueprint.route('/top-tracks', methods=['POST'])
def display_results():
    try:
        lastfm_user = request.form['user']
        period = request.form['time-period']
        track_count = int(request.form['track-count'])
        request_top_tracks(lastfm_user, period, track_count)
        return render_template('display-results.html',
                               user=lastfm_user,
                               period=process_time_period(period),
                               track_count=track_count,
                               songs=return_top_tracks())

    except ValueError as e:
        # Invalid parameters, need to re-enter
        if str(e) == 'user':
            session['home_form_error'] = 'Invalid last.fm user.'
        elif str(e) == 'limit':
            session['home_form_error'] = 'Invalid number of tracks.'
        else:
            session['home_form_error'] = 'Please fill in all the fields.'
        return redirect(url_for('home_bp.home'))

    except AuthenticationError:
        # Spotify authentication expired, need to log in again
        return redirect(url_for('auth_bp.login'))

    except HTTPError:
        return redirect(url_for('home_bp.error'))
