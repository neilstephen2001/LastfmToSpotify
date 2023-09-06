import json

import requests
from flask import session
from requests import HTTPError

from app.domainmodel.model import Song, Playlist
from app.spotify.utilities import make_embedded_url, process_search_results, generate_search_params, generate_header, \
    generate_image_header, get_current_username, generate_playlist_data


class AuthenticationError(Exception):
    def __init__(self, message="Spotify authentication has expired"):
        self.message = message
        super().__init__(self.message)


# Returns the user's top tracks stored in the Flask session
def return_top_tracks():
    return session.get('top_tracks', [])


# Returns the playlist object stored in the Flask session
def return_playlist():
    return session.get('playlist', None)


# Retrieve the song's Spotify URI and the ID of its associated album
def get_uri_and_albums(song: Song):
    # Search for song
    url = f"https://api.spotify.com/v1/search"
    r = requests.get(url=url, headers=generate_header(), params=generate_search_params(song.title, song.artist))

    if r.status_code == 200:
        # Get song URI and album ID (required for adding song to playlist and requesting the cover art, respectively)
        results = r.json()['tracks']['items']
        if not results:
            # No search results retrieved
            song.uri = ""
            song.album_id = ""
        else:
            process_search_results(song, results)

    elif r.status_code == 401:
        # Expired Spotify authentication
        raise AuthenticationError

    else:
        raise HTTPError


# Returns the album image to display with results
def get_album_image(song: Song):
    if song.album_id != "":
        url = f"https://api.spotify.com/v1/albums/{song.album_id}"
        r = requests.get(url=url, headers=generate_header())

        if r.status_code == 200:
            result = r.json()
            song.image_url = result['images'][0]['url']

        elif r.status_code == 401:
            # Expired Spotify authentication
            raise AuthenticationError

        else:
            raise HTTPError


def generate_playlist(name: str, description: str, public: bool = False, cover_art: bytes = None):
    if name == "":
        raise ValueError('playlist_name')

    # Create the playlist
    url = f"https://api.spotify.com/v1/users/{get_current_username()}/playlists"
    r = requests.post(url, data=generate_playlist_data(name, description, public), headers=generate_header())

    if r.status_code == 201:

        # Create playlist object
        result = r.json()
        playlist = Playlist(get_current_username(), result['id'], name, description, public)

        # Add the songs to the playlist
        uri_list = [song['uri'] for song in return_top_tracks()]
        add_songs_to_playlist(playlist, uri_list)

        # Add playlist cover
        if cover_art:
            add_playlist_cover(playlist, cover_art)

        # Generate embedded URL for playlist so it can be displayed
        playlist.url = result['external_urls']['spotify']
        playlist.embedded_url = make_embedded_url(playlist.url)
        session['playlist'] = playlist.to_dict()

    elif r.status_code == 401:
        # Expired Spotify authentication
        raise AuthenticationError

    else:
        print(r.status_code, r.text)
        raise HTTPError


def add_playlist_cover(playlist: Playlist, cover_art: bytes):
    url = f"https://api.spotify.com/v1/playlists/{playlist.id}/images"
    r = requests.put(url, data=cover_art, headers=generate_image_header())

    if r.status_code == 202:
        playlist.cover_art = cover_art

    elif r.status_code == 401:
        # Expired Spotify authentication
        raise AuthenticationError

    else:
        print(r.status_code, r.text)
        raise HTTPError


def add_songs_to_playlist(playlist: Playlist, uri_list: list):
    url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
    r = requests.post(url, data=json.dumps({'uris': uri_list}), headers=generate_header())

    if r.status_code == 201:
        for uri in uri_list:
            playlist.add_song(uri)

    elif r.status_code == 401:
        # Expired Spotify authentication
        raise AuthenticationError

    else:
        print(r.status_code, r.text)
        raise HTTPError
