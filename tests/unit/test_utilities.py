import pytest

from app import config
from app.lastfm.utilities import process_time_period, generate_params


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


def test_process_time_period():
    test_1 = process_time_period('7day')
    test_2 = process_time_period('1month')
    test_3 = process_time_period('3month')
    test_4 = process_time_period('6month')
    test_5 = process_time_period('12month')
    test_6 = process_time_period('overall')
    test_7 = process_time_period('')

    assert test_1 == 'last 7 days'
    assert test_2 == 'last 30 days'
    assert test_3 == 'last 90 days'
    assert test_4 == 'last 180 days'
    assert test_5 == 'last 365 days'
    assert test_6 == 'all-time'
    assert test_7 == 'all-time'
