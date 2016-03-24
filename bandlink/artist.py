import requests

class Artist:
    def __init__(self, spotify, data):
        """Contains info from artist object on Spotify."""
        self.spotify = spotify
        self.id = data['id']
        self.name = data['name']
        self.genres = data['genres']
        self.related = None
        self.related_ids = None
        self.top_tracks = None

        # BFS data
        self.parent1 = self.parent2 = None

        if 'related_ids' in data:
            self.related_ids = data['related_ids']

        if 'top_tracks' in data:
            self.top_tracks = data['top_tracks']


    def get_top_tracks(self):
        if self.top_tracks is not None:
            return self.top_tracks

        print "Querying top tracks..."
        url = 'https://api.spotify.com/v1/artists/{id}/top-tracks' \
            .format(id=self.id)
        data = {
            'country': 'US'
        }
        request = requests.get(
            url=url,
            params=data,
            headers=self.spotify.auth_headers
        )

        tracks = request.json()['tracks']
        self.top_tracks = [track['name'] for track in tracks]
        return self.top_tracks

    def get_related_artists(self):
        if self.related_ids is not None and self.related is None:
            self.related = [self.spotify.cache.get_band_by_id(id) for id in \
                self.related_ids]

        if self.related is not None:
            return self.related

        print "Querying related artists..."
        url = 'https://api.spotify.com/v1/artists/{id}/related-artists' \
            .format(id=self.id)
        request = requests.get(
            url=url,
            headers=self.spotify.auth_headers
        )

        self.related_ids = []
        self.related = []

        for artist in request.json()['artists']:
            new_artist = Artist(self.spotify, artist)
            self.spotify.cache.add_band(new_artist)
            self.related_ids.append(new_artist.id)
            self.related.append(
                self.spotify.cache.get_band_by_id(new_artist.id)
            )
        return self.related

    def __str__(self):
        return \
        'Name: {0}\nID: {1}\nGenres: {2}\n' \
            .format(self.name, self.id, ', '.join(self.genres))
