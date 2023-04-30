"""
last.fm to Spotify playlist maker - Stephen Parinas

main.py:
Contains most of the functions involved with extracting 
the last.fm data and creating the Spotify playlist
"""

import requests
import json
import spotipy

def get_top_tracks(username, time_period, tracks):
    pass

def exceptions(response):
    print("Exception occurred with status code: ", response.status_code)
    print("Error: ", response.text)