import requests
from requests import HTTPError
from app.domainmodel.model import Song
from app.spotify.utilities import make_embedded_url, process_search_results, generate_search_params, generate_header


class AuthenticationError(Exception):
    def __init__(self, message="Spotify authentication has expired"):
        self.message = message
        super().__init__(self.message)


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


"""
def create_playlist(playlist_details, uri_list, cover_art=None):
    access_token = session.get('token_info').get('access_token')
    sp = spotipy.Spotify(auth=access_token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    image_headers = {
        "Content-Type": "image/png",
        "Authorization": f"Bearer {access_token}"
    }
    username = sp.current_user()['id']
    url = f"https://api.spotify.com/v1/users/{username}/playlists"
    r = requests.post(url, data=playlist_details, headers=headers)
    if r.status_code != 201:
        exceptions(r)
    else:
        playlist = r.json()
        if cover_art:
            url = f"https://api.spotify.com/v1/playlists/{playlist['id']}/images"
            req = requests.put(url, data=cover_art, headers=image_headers)
            if req.status_code != 202:
                exceptions(req)
            else:
                print("Playlist cover successfully added")
        url = f"https://api.spotify.com/v1/playlists/{playlist['id']}/tracks"
        uris = json.dumps({'uris': uri_list})
        req = requests.post(url, data=uris, headers=headers)
        if req.status_code != 201:
            exceptions(req)
        else:
            print("Playlist successfully created")
        playlist_url = playlist['external_urls']['spotify']
        embedded_url = make_embedded_url(playlist_url)
        return embedded_url
"""
