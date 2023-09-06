import json
import requests
from flask import session
from requests import HTTPError

from app import config
from app.lastfm.utilities import generate_params, process_track_data
from app.spotify.services import get_uri_and_albums, get_album_image


# Requests the user's top tracks from last.fm
def request_top_tracks(user: str, period: str, limit: int):
    if user == "" or limit is None:
        raise ValueError('incomplete')

    if limit < 1 | limit > 51:
        # Invalid track count submitted
        raise ValueError('limit')

    # Request top track data
    url = 'https://ws.audioscrobbler.com/2.0/'
    header = {'user-agent': config.USER_AGENT}
    r = requests.get(url=url, headers=header, params=generate_params(user, period, limit))

    if r.status_code == 200:
        # Process track data and upload onto Flask session
        result = r.json()
        top_tracks = []
        for track in result['toptracks']['track']:
            song = process_track_data(track)
            get_uri_and_albums(song)
            get_album_image(song)
            top_tracks.append(song.to_dict())
        session['top_tracks'] = top_tracks

    elif (r.status_code == 404) & ((json.loads(r.text)).get('error') == 6):
        # Invalid username submitted
        raise ValueError('user')

    else:
        raise HTTPError


# Returns the user's top tracks stored in the Flask session
def return_top_tracks():
    return session.get('top_tracks', [])




