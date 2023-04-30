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
global lastfm_username
global time_period
global number_of_tracks

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-lastfm', methods=['POST'])
def submit_lastfm():
    return redirect(url_for('results'))

@app.route('/results')
def results():
    lastfm_username = request.form['username']
    time_period = request.form['time-period']
    number_of_tracks = request.form['tracks']
    print(lastfm_username, time_period, number_of_tracks)
    return render_template('display-results.html')

if __name__ == '__main__':
    app.run()