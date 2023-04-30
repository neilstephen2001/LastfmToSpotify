"""
last.fm to Spotify playlist maker - Stephen Parinas

app.py:
Flask app
"""

from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import main

global playlist_url
global embedded_playlist_url
global username
global time_period
global tracks

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-lastfm', methods=['POST'])
def submit_lastfm():
    username = request.form['username']
    time_period = request.form['time-period']
    tracks = request.form['tracks']
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('display-results.html')

@app.route('/return-home', methods=['POST'])
def return_home():
    if 'export' in request.form:
        return render_template('create-playlist.html')
    else:
        return redirect(url_for('index'))

@app.route('/playlist-create', methods=['POST'])
def playlist_create():
    playlist_name = request.form.get('playlist')
    playlist_description = request.form.get('description')
    return redirect(url_for('playlist_display'))

@app.route('/playlist-display')
def playlist_display():
    embedded_playlist_url = "https://open.spotify.com/embed/playlist/000hqMJogZg18TKJHYsidZ?utm_source=generator"
    return render_template('display-playlist.html', value = embedded_playlist_url)

    
if __name__ == '__main__':
    app.run()