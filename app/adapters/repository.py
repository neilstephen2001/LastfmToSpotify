import abc

from app.domainmodel.model import Song

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_song(self, song: Song):
        raise NotImplementedError

    @abc.abstractmethod
    def get_top_songs(self):
        raise NotImplementedError

    @abc.abstractmethod
    def clear_data(self):
        raise NotImplementedError
