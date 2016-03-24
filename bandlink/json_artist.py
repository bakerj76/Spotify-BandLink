from artist import Artist
import json

class ArtistEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Artist):
            return {
                'id': obj.id,
                'name': obj.name,
                'genres': obj.genres,
                'related_ids': obj.related_ids,
                'top_tracks': obj.top_tracks
            }

        return json.JSONEncoder.default(self, obj)
