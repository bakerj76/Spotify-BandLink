import requests

class Youtube:
    def __init__(self, key):
        self.__key = key

    def search(self, query):
        data = {
            'part': 'snippet',
            'maxResults': 1,
            'q': query,
            'type': 'video',
            'key': self.__key
        }

        request = requests.get(
            url='https://www.googleapis.com/youtube/v3/search',
            params=data
        )

        result = request.json()

        if result['pageInfo']['totalResults'] > 0:
            return result['items'][0]['id']['videoId']

        return None


    def id_to_link(self, video_id):
        return 'https://www.youtube.com/watch?v={0}'.format(video_id)

    def ids_to_playlist(self, video_ids):
        return 'http://www.youtube.com/watch_videos?video_ids={0}' \
            .format(','.join(video_ids))
