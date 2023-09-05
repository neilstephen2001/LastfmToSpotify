import json
import requests
from requests import HTTPError

from app.adapters.repository import AbstractRepository
from app.lastfm.utilities import generate_link, generate_header, generate_params, process_track_data


# Returns the user's top tracks from last.fm
def request_top_tracks(user: str, period: str, limit: int, repo: AbstractRepository):
    if limit < 1 | limit > 50:
        # Invalid track count submitted
        raise ValueError('limit')

    # Request top track data
    r = requests.get(url=generate_link(), headers=generate_header(),
                     params=generate_params(user, period, limit))

    if r.status_code == 200:
        # Process track data and upload onto memory repository
        repo.clear_data()
        response = r.json()
        for track in response['toptracks']['track']:
            repo.add_song(process_track_data(track))

    elif r.status_code == 404 & (json.loads(r.text)).get('error') == 6:
        # Invalid username submitted
        raise ValueError('user')

    else:
        raise HTTPError


def return_top_tracks(repo: AbstractRepository):
    return repo.get_top_songs()




