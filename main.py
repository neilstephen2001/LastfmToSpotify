"""
last.fm to Spotify playlist maker - Stephen Parinas

main.py:
Contains most of the functions involved with extracting 
the last.fm data and creating the Spotify playlist
"""

import requests
import json
import spotipy
import config

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
        return organise_data(r)

def organise_data(response):
    track_data = []
    r = response.json()
    for track in r['toptracks']['track']:
        data = {
            'track_name': track['name'],
            'playcount': track['playcount'],
            'url': track['url'],
            'artist_name': track['artist']['name'],
            'image': track['image'][2]['#text']
        }
        track_data.append(data)
    return track_data

def get_headers():
    username = config.SPOTIFY_USERNAME
    scope = 'playlist-modify-private'
    spotify_id = config.SPOTIFY_ID
    spotify_secret = config.SPOTIFY_SECRET
    redirect_uri = config.SPOTIFY_REDIRECT_URI
    token = spotipy.util.prompt_for_user_token(username, scope, spotify_id, spotify_secret, redirect_uri)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer { token }"
    }
    return headers

def get_song_uri(track_data):
    uri_list = []
    for i in range(len(track_data)):
        item = track_data[i]
        # remove punctuation as spotify does not recognise it when searching
        song = remove_punctuation(item['track_name'])
        artist = remove_punctuation(item['artist_name'])

        url = f"https://api.spotify.com/v1/search?query=track%3A{song}+artist%3A{artist}&type=track&offset=0&limit=5"
        r = requests.get(url = url, headers = get_headers())

        if r.status_code != 200:
            exceptions(r)
            break
        else:
            uri = r.json()['tracks']['items']
            if not uri:
                break
            # find matching song out of the top 5 results
            # if none match, pick the top result
            for i in range(5):
                if len(item['track_name']) == len(uri[i]['name']):
                    uri_list.append(uri[i]['uri'])
                    break
                elif i == 4:
                    uri_list.append(uri[0]['uri'])
    return uri_list

def create_playlist(playlist_details, uri_list):
    url = f"https://api.spotify.com/v1/users/{config.SPOTIFY_USERNAME}/playlists"
    r = requests.post(url, data=playlist_details, headers=get_headers())
    if r.status_code != 201:
        exceptions(r)
    else:
        playlist = r.json()
        add_songs_to_playlist(playlist['id'], uri_list)
        playlist_url = playlist['external_urls']['spotify']
        embedded_url = make_embedded_url(playlist_url)
        return embedded_url

def add_songs_to_playlist(playlist_id, uri_list):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    data = json.dumps({'uris': uri_list})
    r = requests.post(url, data = data, headers=get_headers())
    if r.status_code != 201:
        exceptions(r)
    else:
        print("Playlist successfully created")

def remove_punctuation(name):
    punctuation = '''{};:'"\,<>/@#$%^&*_~'''
    for i in name:
        if i in punctuation:
            if i == '&':
                name = name.replace(i, 'and')
            else:
                name = name.replace(i, "")
    return name

def make_embedded_url(playlist_url):
    split_url = playlist_url.partition(".com/")
    embedded_url = split_url[0] + split_url[1] + 'embed/' + split_url[2] + '?utm_source=generator'
    return embedded_url

def exceptions(response):
    print("Exception occurred with status code: ", response.status_code)
    print("Error: ", response.text)