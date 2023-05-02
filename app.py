"""
last.fm to Spotify playlist maker - Stephen Parinas

app.py:
Flask app
"""

from flask import Flask, request, url_for, session, redirect, render_template, jsonify
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests
import json
import config
import base64

"""FLASK APP"""
app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def login():
    sp_oauth = SpotifyOAuth(client_id=config.SPOTIFY_ID,
                            client_secret=config.SPOTIFY_SECRET,
                            redirect_uri=config.SPOTIFY_REDIRECT_URL,
                            scope=['playlist-modify-private', 'playlist-modify-public', 'ugc-image-upload'],
                            show_dialog=True)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    sp_oauth = SpotifyOAuth(client_id=config.SPOTIFY_ID,
                            client_secret=config.SPOTIFY_SECRET,
                            redirect_uri=config.SPOTIFY_REDIRECT_URL,
                            scope=['playlist-modify-private', 'playlist-modify-public', 'ugc-image-upload'],
                            show_dialog=True)
    session.clear()
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))

@app.route('/home')
def index():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')

@app.route('/submit-lastfm', methods=['POST'])
def submit_lastfm():
    global username 
    global time_period
    global tracks

    username = request.form['username']
    time_period = request.form['time-period']
    tracks = request.form['tracks']
    return redirect(url_for('get_data'))

@app.route('/get-data')
def get_data():
    global track_data
    track_data = get_top_tracks(user = username, period = time_period, limit = tracks)
    global song_uri
    song_uri, album_list = get_song_uri(track_data)
    get_album_image(album_list, track_data)
    return redirect(url_for('results'))

@app.route('/process-data')
def process_data():
    return jsonify(track_data)
    
@app.route('/results')
def results():
    if time_period == '7day':
        period = 'last 7 days'
    elif time_period == '1month':
        period = 'last 30 days'
    elif time_period == '3month':
        period = 'last 90 days'
    elif time_period == '6month':
        period = 'last 180 days'
    elif time_period == '12month':
        period = 'last 365 days'
    else:
        period = 'all-time'
    return render_template('display-results.html', username = username, tracks = tracks, period = period)

@app.route('/export-playlist', methods=['POST'])
def export_playlist():
    if 'export' in request.form:
        return render_template('create-playlist.html')
    else:
        return redirect(url_for('index'))

@app.route('/playlist-create', methods=['POST'])
def playlist_create():
    global embedded_playlist_url
    playlist_details = json.dumps({
        'name': request.form.get('playlist-name'),
        'description': request.form.get('description'),
        'public': False
    })
    cover_art = request.files['cover-art']
    encoded_image = base64.b64encode(cover_art.read())
    embedded_playlist_url = create_playlist(playlist_details, song_uri, encoded_image)
    return redirect(url_for('playlist_display'))

@app.route('/playlist-display')
def playlist_display():
    return render_template('display-playlist.html', value = embedded_playlist_url)

@app.route('/return-home', methods=['POST'])
def return_home():
    return redirect(url_for('index'))


"""OTHER FUNCTIONS"""

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


# Returns the Spotify URI for each of the user's top songs
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


# Creates an empty playlist then adds the user's top songs
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


if __name__ == '__main__':
    app.run()
