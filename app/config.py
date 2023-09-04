from decouple import config

"""Flask app configuration"""
TESTING = True
DEBUG = False
FLASK_ENV = 'development'
SECRET_KEY = 'stan_exo'

"""Secret keys"""
USER_AGENT = "stvn127"
LASTFM_API = config('LASTFM_API')
SPOTIFY_ID = config('SPOTIFY_ID')
SPOTIFY_SECRET = config('SPOTIFY_SECRET')
SPOTIFY_REDIRECT_URL = config('SPOTIFY_REDIRECT_URL')