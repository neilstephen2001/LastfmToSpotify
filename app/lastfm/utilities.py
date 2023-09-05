from app import config
from app.domainmodel.model import Song


def generate_link():
    return 'https://ws.audioscrobbler.com/2.0/'


def generate_header():
    return {'user-agent': config.USER_AGENT}


def generate_params(user: str, period: str, limit: int):
    return {
        'api_key': config.LASTFM_API,
        'method': "user.getTopTracks",
        'format': 'json',
        'user': user,
        'period': period,
        'limit': limit
    }


def process_track_data(track):
    song = Song(int(track['@attr']['rank']))
    song.title = track['name']
    song.artist = track['artist']['name']
    song.playcount = int(track['playcount'])
    return song


def process_time_period(time_period: str):
    if time_period == '7day':
        return 'last 7 days'
    elif time_period == '1month':
        return 'last 30 days'
    elif time_period == '3month':
        return 'last 90 days'
    elif time_period == '6month':
        return 'last 180 days'
    elif time_period == '12month':
        return 'last 365 days'
    else:
        return 'all-time'
