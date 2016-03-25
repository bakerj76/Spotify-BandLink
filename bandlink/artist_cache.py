from json_artist import ArtistEncoder
from spotify.artist import Artist

import json
import logging

ID_FILE = 'id.json'
ARTIST_FILE = 'artist.json'

class ArtistCache:
    def __init__(self, spotify):
        self.spotify = spotify
        self.load()

    def id_in_cache(self, id):
        return id in self.__artist_table

    def band_in_cache(self, name):
        return name in self.__artist_id

    def get_band(self, name):
        return self.__artist_table[self.__artist_id[name]]

    def get_band_by_id(self, id):
        if id in self.__artist_table:
            return self.__artist_table[id]

        return self.spotify.find_artist_by_id(id)

    def add_band(self, artist):
        if self.band_in_cache(artist.name):
            return

        self.__artist_id[artist.name] = artist.id
        self.__artist_table[artist.id] = artist

    def save(self):
        logging.info('Saving results...')
        
        with open(ID_FILE, 'wb') as f:
            json.dump(self.__artist_id, f)

        with open(ARTIST_FILE, 'wb') as f:
            json.dump(self.__artist_table, f, cls=ArtistEncoder)

    def load(self):
        with open(ID_FILE, 'a+') as f:
            try:
                self.__artist_id = json.load(f)
            except ValueError:
                self.__artist_id = {}

        with open(ARTIST_FILE, 'a+') as f:
            try:
                artist_table = json.load(f)
                self.__artist_table = {}

                for k, v in artist_table.iteritems():
                    self.__artist_table[k] = Artist(self.spotify, v)

            except ValueError:
                self.__artist_table = {}
