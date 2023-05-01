import os

"""Flask app configuration"""
TESTING = True
DEBUG = False
FLASK_ENV = 'development'

"""Secret keys"""
USER_AGENT = "stvn127"
LASTFM_API = os.environ.get('LASTFM_API')
LASTFM_SECRET = os.environ.get('LASTFM_SECRET')
SPOTIFY_ID = os.environ.get('SPOTIFY_ID')
SPOTIFY_SECRET = os.environ.get('SPOTIFY_SECRET')
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:5000/callback"
SPOTIFY_USERNAME = "kfs3lqp4ixq8klhnmk8qh50sj"