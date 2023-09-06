class Song:
    def __init__(self, rank: int):
        if type(rank) is not int or rank < 0:
            raise ValueError("Invalid track ranking")
        self.__rank = rank
        self.__title = None
        self.__artist = None
        self.__playcount = None
        self.__image_url = None
        self.__uri = None
        self.__album_id = None

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
    def image_url(self) -> str:
        return self.__image_url

    @image_url.setter
    def image_url(self, image_url: str):
        if isinstance(image_url, str):
            self.__image_url = image_url
        else:
            self.__image_url = None

    @property
    def uri(self) -> str:
        return self.__uri

    @uri.setter
    def uri(self, uri: str):
        if isinstance(uri, str):
            self.__uri = uri
        else:
            self.__uri = None

    @property
    def album_id(self) -> str:
        return self.__album_id

    @album_id.setter
    def album_id(self, album_id: str):
        if isinstance(album_id, str):
            self.__album_id = album_id
        else:
            self.__album_id = None

    def to_dict(self):
        return {
            'rank': self.__rank,
            'title': self.__title,
            'artist': self.__artist,
            'playcount': self.__playcount,
            'image_url': self.__image_url,
            'uri': self.__uri,
            'album_id': self.__album_id
        }

    def __repr__(self):
        return f'<Song {self.__rank}. {self.__artist} - {self.__title}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.__rank == other.rank) & (self.__title == other.__title) & (self.__artist == other.__artist)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__rank < other.rank


class Playlist:

    def __init__(self, user: str, id: str, name: str, description: str, public: bool):
        if isinstance(user, str):
            self.__user = user
        else:
            self.__user = ""

        if isinstance(id, str):
            self.__id = id
        else:
            self.__id = ""

        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = None

        if isinstance(description, str):
            self.__description = description
        else:
            self.__description = None

        if isinstance(public, bool):
            self.__public = public
        else:
            self.__public = None

        self.__cover_art = None
        self.__url = None
        self.__embedded_url = None
        self.__songs_list = []

    @property
    def user(self) -> str:
        return self.__user

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def public(self) -> bool:
        return self.__public

    @property
    def cover_art(self) -> str:
        return self.__cover_art

    @cover_art.setter
    def cover_art(self, cover_art: str):
        if isinstance(cover_art, str):
            self.__cover_art = cover_art
        else:
            self.__cover_art = None

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
    def embedded_url(self) -> str:
        return self.__embedded_url

    @embedded_url.setter
    def embedded_url(self, embedded_url: str):
        if isinstance(embedded_url, str):
            self.__embedded_url = embedded_url
        else:
            self.__embedded_url = None

    @property
    def songs_list(self) -> list:
        return self.__songs_list

    def add_song(self, song: Song):
        if not isinstance(song, Song) or song in self.__songs_list:
            return
        self.__songs_list.append(song)

    def to_dict(self):
        return {
            'user': self.__user,
            'id': self.__id,
            'name': self.__name,
            'description': self.__description,
            'cover_art': self.__cover_art,
            'url': self.__url,
            'embedded_url': self.__embedded_url,
            'songs_list': self.__songs_list
        }

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.__user == other.user) & (self.__name == other.__name)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.__user < other.__user:
            return True
        elif self.__user > other.__user:
            return False
        return self.__name < other.name
