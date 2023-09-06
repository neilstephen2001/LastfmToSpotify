import pytest

from app import config, create_app
from app.domainmodel.model import Song
from app.lastfm.utilities import process_time_period, generate_params, process_track_data
from app.spotify.utilities import generate_header, generate_image_header


# lastfm utilities
def test_generate_params():
    params = generate_params('stvn127', '7-days', 10)
    test_params = {'api_key': config.LASTFM_API,
                   'method': "user.getTopTracks",
                   'format': 'json',
                   'user': 'stvn127',
                   'period': '7-days',
                   'limit': 10}
    assert params == test_params


def test_process_track_data():
    track_json = {
        '@attr': {'rank': '1'},
        'name': 'good 4 u',
        'artist': {'name': 'Olivia Rodrigo'},
        'playcount': '1989'
    }
    song = Song(1, 'good 4 u', 'Olivia Rodrigo', 1989)
    assert process_track_data(track_json) == song


def test_process_time_period():
    assert process_time_period('7day') == 'last 7 days'
    assert process_time_period('1month') == 'last 30 days'
    assert process_time_period('3month') == 'last 90 days'
    assert process_time_period('6month') == 'last 180 days'
    assert process_time_period('12month') == 'last 365 days'
    assert process_time_period('overall') == 'all-time'
    assert process_time_period('') == 'all-time'


# Spotify utilities
def test_generate_header():
    pass


def test_generate_image_header():
    pass


def test_get_current_username():
    pass


def test_generate_search_params():
    pass


def test_process_search_results():
    pass


def test_generate_playlist_data():
    pass


def test_make_embedded_url():
    pass