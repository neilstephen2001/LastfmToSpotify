"""
last.fm to Spotify playlist maker - Stephen Parinas

main.py:
Contains most of the functions involved with extracting 
the last.fm data and creating the Spotify playlist
"""
from spotipy.oauth2 import SpotifyOAuth
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

def create_spotify_oauth():
    return SpotifyOAuth(client_id=config.SPOTIFY_ID,
                            client_secret=config.SPOTIFY_SECRET,
                            redirect_uri=config.SPOTIFY_REDIRECT_URI,
                            scope=['playlist-modify-private', 'playlist-modify-public'])

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
    artist_list = []
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
            print(song, artist)
            uri = r.json()['tracks']['items']
            if not uri:
                artist_list.append({'id': ""})
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
                        artist_list.append(uri[i]['artists'][0])
                        break
                    elif i == 4:
                        uri_list.append(uri[0]['uri'])
                        artist_list.append(uri[i]['artists'][0])
    return uri_list, artist_list

def get_artist_image(artist_list, track_data):
    for i in range(len(artist_list)):
        artist_id = artist_list[i]['id']
        if artist_id != "":
            url = f"https://api.spotify.com/v1/artists/{artist_id}"
            r = requests.get(url = url, headers = get_headers())

            if r.status_code != 200:
                exceptions(r)
                break
            else:
                track_data[i]['image'] = r.json()['images'][0]['url']

def remove_punctuation(name):
    punctuation = """{};:'",<>@#$%^&*_~"""
    for i in name:
        if i in punctuation:
            if i == '&':
                name = name.replace(i, 'and')
            elif i == '/' or i == '\\':
                name = name.replace(i, " ")
            else:
                name = name.replace(i, "")
    return name

def make_embedded_url(playlist_url):
    split_url = playlist_url.partition(".com/")
    embedded_url = split_url[0] + split_url[1] + 'embed/' + split_url[2] + '?utm_source=generator&theme=0'
    return embedded_url

def exceptions(response):
    print("Exception occurred with status code: ", response.status_code)
    print("Error: ", response.text)
