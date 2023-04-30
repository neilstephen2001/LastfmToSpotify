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
    return redirect(url_for('results'))

@app.route('/results', methods=['GET'])
def results():
    return 'hi'


if __name__ == '__main__':
    app.run()