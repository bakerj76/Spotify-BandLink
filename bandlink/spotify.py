from artist import Artist
from artist_cache import ArtistCache

import base64
import requests

class Spotify:
    def __init__(self, client_id, secret):
        self.cache = ArtistCache(self)
        self.__init_headers(client_id, secret)
        self.__setup_auth_headers()

    def __init_headers(self, client_id, secret):
        """Initialize the token POST headers/data to get the access token."""
        self.__token_headers = {
            'Authorization': 'Basic ' + \
                base64.b64encode(client_id + ':' + secret)
        }

        self.__token_data = {
            'grant_type': 'client_credentials'
        }

    def __setup_auth_headers(self):
        """Gets the access token and sets up the authorization headers."""
        request = requests.post(
            url='https://accounts.spotify.com/api/token',
            data=self.__token_data,
            headers=self.__token_headers
        )

        response = request.json()
        print response

        self.auth_headers = {
            'Authorization': 'Bearer ' + response['access_token']
        }

    def find_artist_by_id(self, id):
        if self.cache.id_in_cache(id):
            return self.get_band_by_id(id)

        print 'Querying {0}...'.format(id)
        request = requests.get(
            url='https://api.spotify.com/v1/artists/{id}'.format(id=id),
            headers=self.auth_headers
        )

        artist = Artist(self, request.json())
        self.cache.add_band(artist)
        return artist


    def find_artist(self, name):
        if self.cache.band_in_cache(name):
            return self.cache.get_band(name)

        print u'Querying {0}...'.format(name)

        data = {
            'q': name.replace(' ', '+'),
            'type': 'artist'
        }

        # Search for the artist.
        request = requests.get(
            url='https://api.spotify.com/v1/search',
            params=data,
            headers=self.auth_headers
        )

        # Get the results.
        items = request.json()['artists']['items']

        if len(items) > 0:
            # Return the first found artist.
            artist = Artist(self, items[0])
            self.cache.add_band(artist)
            return artist
        else:
            raise Exception("Band not found!")
