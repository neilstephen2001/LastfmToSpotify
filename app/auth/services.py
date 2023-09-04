from spotipy import SpotifyOAuth, SpotifyOauthError

from app import config


def create_spotify_oauth():
    try:
        sp_oauth = SpotifyOAuth(client_id=config.SPOTIFY_ID,
                                client_secret=config.SPOTIFY_SECRET,
                                redirect_uri=config.SPOTIFY_REDIRECT_URL,
                                scope=['playlist-modify-private', 'playlist-modify-public', 'ugc-image-upload'],
                                show_dialog=True)
        return sp_oauth

    except SpotifyOauthError as e:
        # client ID, client secret or redirect URL are not set
        print(f"{type(e).__name__}: {str(e)}")
        return None

    except AttributeError as e:
        # incorrect attribute name
        print(f"{type(e).__name__}: {str(e)}")
        return None
