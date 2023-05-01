"""
last.fm to Spotify playlist maker - Stephen Parinas

app.py:
Flask app
"""

from flask import Flask, request, url_for, session, redirect, render_template, jsonify
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import time
import requests
import json
import config, main

# Flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'stan_exo'

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(client_id=config.SPOTIFY_ID,
                            client_secret=config.SPOTIFY_SECRET,
                            redirect_uri=config.SPOTIFY_REDIRECT_URI,
                            scope=['playlist-modify-private', 'playlist-modify-public'],
                            cache_path='cache',
                            show_dialog=True)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    print('Redirected')
    sp_oauth = SpotifyOAuth(client_id=config.SPOTIFY_ID,
                            client_secret=config.SPOTIFY_SECRET,
                            redirect_uri=config.SPOTIFY_REDIRECT_URI,
                            scope=['playlist-modify-private', 'playlist-modify-public'],
                            cache_path='cache',
                            show_dialog=True)
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))

@app.route('/')
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
    track_data = main.get_top_tracks(user = username, period = time_period, limit = tracks)
    global song_uri
    song_uri, artist_list = main.get_song_uri(track_data)
    main.get_artist_image(artist_list, track_data)
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
    embedded_playlist_url = main.create_playlist(playlist_details, song_uri)
    return redirect(url_for('playlist_display'))

@app.route('/playlist-display')
def playlist_display():
    return render_template('display-playlist.html', value = embedded_playlist_url)

@app.route('/return-home', methods=['POST'])
def return_home():
    return redirect(url_for('index'))

# other functions
def create_playlist(playlist_details, uri_list):
    token_info = spotipy.Spotify(auth=session.get('token_info'))
    sp = token_info.get('access_token')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer { sp }"
    }
    username = sp.me()['id']
    url = f"https://api.spotify.com/v1/users/{username}/playlists"
    r = requests.post(url, data=playlist_details, headers=headers)
    if r.status_code != 201:
        main.exceptions(r)
    else:
        playlist = r.json()
        add_songs_to_playlist(playlist['id'], uri_list)
        playlist_url = playlist['external_urls']['spotify']
        embedded_url = main.make_embedded_url(playlist_url)
        return embedded_url

def add_songs_to_playlist(playlist_id, uri_list):
    token_info = spotipy.Spotify(auth=session.get('token_info'))
    sp = token_info.get('access_token')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer { sp }"
    }
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    data = json.dumps({'uris': uri_list})
    r = requests.post(url, data = data, headers=headers)
    if r.status_code != 201:
        main.exceptions(r)
    else:
        print("Playlist successfully created")

if __name__ == '__main__':
    app.run()
