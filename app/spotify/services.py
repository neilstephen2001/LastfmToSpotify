import json

import requests
from requests import HTTPError

from app.adapters.repository import AbstractRepository
from app.domainmodel.model import Song, Playlist
from app.spotify.utilities import make_embedded_url, process_search_results, generate_search_params, generate_header, \
    generate_image_header, get_current_username


class AuthenticationError(Exception):
    def __init__(self, message="Spotify authentication has expired"):
        self.message = message
        super().__init__(self.message)


# Returns the user's top tracks stored in the memory repository
def return_top_tracks(repo: AbstractRepository):
    return repo.get_top_songs()


# Returns the playlist object stored in the memory repository
def return_playlist(repo: AbstractRepository):
    return repo.get_playlist()


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


def generate_playlist(repo: AbstractRepository, playlist_details, cover_art=None):
    # Create the playlist
    url = f"https://api.spotify.com/v1/users/{get_current_username()}/playlists"
    r = requests.post(url, data=playlist_details, headers=generate_header())

    if r.status_code == 201:

        # Create playlist object
        result = r.json()
        playlist = Playlist(get_current_username(), result['id'])
        repo.set_playlist(playlist)

        # Add the songs to the playlist
        uri_list = json.dumps({'uris': [song.uri for song in return_top_tracks(repo)]})
        add_songs_to_playlist(playlist, uri_list)

        # Add playlist cover
        if cover_art:
            add_playlist_cover(playlist, cover_art)

        # Generate embedded URL for playlist so it can be displayed
        playlist_url = result['external_urls']['spotify']
        playlist.embedded_url = make_embedded_url(playlist_url)

    elif r.status_code == 401:
        # Expired Spotify authentication
        raise AuthenticationError

    else:
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
        raise HTTPError


def add_songs_to_playlist(playlist: Playlist, uri_list: list):
    url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
    r = requests.post(url, data=uri_list, headers=generate_header())

    if r.status_code == 201:
        for uri in uri_list:
            playlist.add_song(uri)

    elif r.status_code == 401:
        # Expired Spotify authentication
        raise AuthenticationError

    else:
        raise HTTPError
