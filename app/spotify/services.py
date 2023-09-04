import json

import requests
import spotipy
from flask import session

from app.spotify.utilities import remove_punctuation, make_embedded_url, exceptions


def get_song_uri(track_data):
    access_token = session.get('token_info').get('access_token')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer { access_token }"
    }
    uri_list = []
    album_list = []
    for i in range(len(track_data)):
        item = track_data[i]
        # remove punctuation as spotify does not recognise it when searching
        song = remove_punctuation(item['track_name'])
        artist = remove_punctuation(item['artist_name'])

        url = f"https://api.spotify.com/v1/search?query=track%3A{song}+artist%3A{artist}&type=track&offset=0&limit=5"
        r = requests.get(url = url, headers = headers)

        if r.status_code != 200:
            exceptions(r)
            break
        else:
            uri = r.json()['tracks']['items']
            if not uri:
                album_list.append({'id': ""})
                uri_list.append("")
            else:
                # find matching song out of the top 3 results
                # if none match, pick the top result
                top_results = 5
                if len(uri) < 5:
                    top_results = len(uri)
                for i in range(top_results):
                    if len(item['track_name']) == len(uri[i]['name']):
                        uri_list.append(uri[i]['uri'])
                        album_list.append(uri[i]['album'])
                        break
                    elif i == 4:
                        uri_list.append(uri[0]['uri'])
                        album_list.append(uri[i]['album'])
    return uri_list, album_list


def create_playlist(playlist_details, uri_list, cover_art = None):
    access_token = session.get('token_info').get('access_token')
    sp = spotipy.Spotify(auth=access_token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer { access_token }"
    }
    image_headers = {
        "Content-Type": "image/png",
        "Authorization": f"Bearer { access_token }"
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
            req = requests.put(url, data = cover_art, headers=image_headers)
            if req.status_code != 202:
                exceptions(req)
            else:
                print("Playlist cover successfully added")
        url = f"https://api.spotify.com/v1/playlists/{playlist['id']}/tracks"
        uris = json.dumps({'uris': uri_list})
        req = requests.post(url, data = uris, headers=headers)
        if req.status_code != 201:
            exceptions(req)
        else:
            print("Playlist successfully created")
        playlist_url = playlist['external_urls']['spotify']
        embedded_url = make_embedded_url(playlist_url)
        return embedded_url