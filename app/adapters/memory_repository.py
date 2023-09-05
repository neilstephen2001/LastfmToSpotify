from bisect import insort_left

from app.adapters.repository import AbstractRepository
from app.domainmodel.model import Song


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__songs = list()

    def add_song(self, song: Song):
        if isinstance(song, Song) and song not in self.__songs:
            insort_left(self.__songs, song)

    def clear_data(self):
        self.__songs.clear()


def generate_songs_list(songs_list: list, repo: MemoryRepository):
    for song in songs_list:
        repo.add_song(song)
