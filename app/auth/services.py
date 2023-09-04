from spotipy import SpotifyOAuth

from app import config


def create_spotify_oauth():
    return SpotifyOAuth(client_id=config.SPOTIFY_ID,
                        client_secret=config.SPOTIFY_SECRET,
                        redirect_uri=config.SPOTIFY_REDIRECT_URL,
                        scope=['playlist-modify-private', 'playlist-modify-public', 'ugc-image-upload'],
                        show_dialog=True)
