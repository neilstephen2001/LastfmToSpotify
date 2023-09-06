import json

import spotipy
from flask import session
import urllib.parse

from app.domainmodel.model import Song


# Header for requesting Spotify data (requires authentication)
def generate_header():
    access_token = session.get('token_info').get('access_token')
    return {"Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"}


def generate_image_header():
    access_token = session.get('token_info').get('access_token')
    return {"Content-Type": "image/jpeg",
            "Authorization": f"Bearer {access_token}"}


def get_current_username():
    access_token = session.get('token_info').get('access_token')
    sp = spotipy.Spotify(auth=access_token)
    return sp.current_user()['id']


def generate_search_params(title: str, artist: str):
    return {'q': f'track:{title} artist:{artist}', 'type': 'track', 'limit': 5}


def process_search_results(song: Song, results):
    top_results = len(results) if len(results) < 5 else 5

    # find matching song out of the top results (maximum 5)
    # if none match, pick the first result
    for i in range(top_results):
        if len(song.title) == len(results[i]['name']):
            song.uri = results[i]['uri']
            song.album_id = results[i]['album']['id']
            break
        elif i == top_results - 1:
            song.uri = results[0]['uri']
            song.album_id = results[0]['album']['id']


def generate_playlist_data(name: str, description: str, public: bool):
    return json.dumps({'name': name, 'description': description, 'public': public})


# Generate URL for embedding playlist onto page
def make_embedded_url(playlist_url: str):
    split_url = playlist_url.partition(".com/")
    embedded_url = split_url[0] + split_url[1] + 'embed/' + split_url[2] + '?utm_source=generator&theme=0'
    return embedded_url



