from spotify import Spotify
from bandlink.youtube import Youtube

import logging
import os
import random
import sys

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']
YOUTUBE_KEY = os.environ['YOUTUBE_KEY']

def find_link(spotify, artist1, artist2):
    a1 = spotify.find_artist(artist1)
    a2 = spotify.find_artist(artist2)

    goal = bfs_both(a1, a2)

    # No link found.
    if goal is None:
        return None

    path = []

    temp = goal
    while temp is not None:
        path.append(temp)
        temp = temp.parent1

    path.reverse()

    temp = goal.parent2
    while temp is not None:
        path.append(temp)
        temp = temp.parent2

    return path

def bfs_both(artist1, artist2):
    q1 = [artist1]
    q2 = [artist2]
    marked1 = set([artist1.id])
    marked2 = set([artist2.id])

    while len(q1) > 0 or len(q2) > 0:
        if len(q1) > 0:
            found = bfs(q1, marked1, marked2)
            if found is not None:
                return found

        if len(q2) > 0:
            found = bfs(q2, marked2, marked1)
            if found is not None:
                return found

def bfs(queue, this_marked, other_marked):
    node = queue.pop()

    logging.info(u'Visiting {0}...' \
        .format(node.name) \
        .encode(sys.stdout.encoding, errors='replace'))

    for related_artist in node.get_related_artists():
        if related_artist.id not in this_marked:
            related_artist.parent2 = node

            if related_artist.id in other_marked:
                logging.info("Found goal!")
                return related_artist

            this_marked.add(related_artist.id)
            queue.insert(0, related_artist)

def get_random_tracks(path):
    tracks = []

    for band in path:
        top_tracks = band.get_top_tracks()
        if len(top_tracks) == 0:
            tracks.append((band.name, ''))
        else:
            tracks.append((band.name, random.choice(top_tracks)))

    return tracks

def get_youtube_videos(youtube, tracks):
    ids = []

    for track in tracks:
        video = youtube.search(track[0] + ' ' + track[1])
        print u'{0} - {1}'.format(track[0], track[1])\
            .encode(sys.stdout.encoding, errors='replace')

        if video is not None:
            print '({0})'.format(youtube.id_to_link(video))
            ids.append(video)

    print '\nPlaylist: {0}'.format(youtube.ids_to_playlist(ids))

def main(args=None):
    logging.basicConfig(filename='bandlink.log', level=logging.INFO)

    if args is None:
        args = sys.argv[1:]

    if len(args) < 2:
        print "Usage: bandlink [band1] [band2]"
        return

    spotify = Spotify(SPOTIFY_CLIENT_ID, SPOTIFY_SECRET)
    youtube = Youtube(YOUTUBE_KEY)
    path = find_link(spotify, args[0], args[1])

    if path is None:
        print "Link not found!"

    tracks = get_random_tracks(path)
    get_youtube_videos(youtube, tracks)

    spotify.cache.save()

if __name__ == '__main__':
    main()
