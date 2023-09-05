from bisect import insort_left

from app.adapters.repository import AbstractRepository
from app.domainmodel.model import Song


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__songs = list()

    def add_song(self, song: Song):
        if isinstance(song, Song) and song not in self.__songs:
            insort_left(self.__songs, song)

    def get_top_songs(self):
        return self.__songs

    def clear_data(self):
        self.__songs.clear()
