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

@app.route('/')
def index():
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
    global song_uri
    song_uri, artist_list = main.get_song_uri(track_data)
    main.get_artist_image(artist_list, track_data)
    return render_template('display-results.html', username = username, tracks = tracks, period = period)

@app.route('/return-home', methods=['POST'])
def return_home():
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

if __name__ == '__main__':
    app.run()
