class Song:
    def __init__(self):
        self.__title = None
        self.__artist = None
        self.__rank = None
        self.__playcount = None
        self.__url = None
        self.__uri_list = []
        self.__album_list = []

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        if isinstance(title, str):
            self.__title = title
        else:
            self.__title = None

    @property
    def artist(self) -> str:
        return self.__artist

    @artist.setter
    def artist(self, artist: str):
        if isinstance(artist, str):
            self.__artist = artist
        else:
            self.__artist = None

    @property
    def rank(self) -> int:
        return self.__rank

    @rank.setter
    def rank(self, rank: int):
        if isinstance(rank, int):
            self.__rank = rank
        else:
            self.__rank = None

    @property
    def playcount(self) -> int:
        return self.__playcount

    @playcount.setter
    def playcount(self, playcount: int):
        if isinstance(playcount, int):
            self.__playcount = playcount
        else:
            self.__playcount = None

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str):
        if isinstance(url, str):
            self.__url = url
        else:
            self.__url = None

    @property
    def uri_list(self) -> list:
        return self.__uri_list

    @property
    def album_list(self) -> list:
        return self.__album_list

    def add_uri(self, uri: str):
        if not isinstance(uri, str) or uri in self.__uri_list:
            return
        self.__uri_list.append(uri)

    def add_album(self, album: str):
        if not isinstance(album, str) or album in self.__album_list:
            return
        self.__uri_list.append(album)