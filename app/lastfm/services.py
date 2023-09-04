import requests
import spotipy
from flask import session

from app import config
from app.spotify.utilities import exceptions


# Returns the user's top tracks from last.fm
def get_top_tracks(user, period, limit):
    headers = {
        'user-agent': config.USER_AGENT
    }
    payload = {
        'api_key': config.LASTFM_API,
        'method': "user.getTopTracks",
        'format': 'json',
        'user': user,
        'period': period,
        'limit': limit
    }
    r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
    if r.status_code != 200:
        exceptions(r)
    else:
        track_data = []
        response = r.json()
        for track in response['toptracks']['track']:
            data = {
                'rank': track['@attr']['rank'],
                'track_name': track['name'],
                'playcount': track['playcount'],
                'url': track['url'],
                'artist_name': track['artist']['name'],
            }
            track_data.append(data)
        return track_data


# Returns the album images to display with results
def get_album_image(album_list, track_data):
    access_token = session.get('token_info').get('access_token')
    sp = spotipy.Spotify(auth=access_token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer { access_token }"
    }
    for i in range(len(album_list)):
        album_id = album_list[i]['id']
        if album_id != "":
            url = f"https://api.spotify.com/v1/albums/{album_id}"
            r = requests.get(url = url, headers = headers)

            if r.status_code != 200:
                exceptions(r)
                break
            else:
                track_data[i]['image'] = r.json()['images'][0]['url']