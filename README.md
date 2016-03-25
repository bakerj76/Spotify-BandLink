# Spotify-BandLink
A Spotify-MixtUp/MixMates rip off that gives you Youtube links and a playlist.

BandLink finds a path of related artists between two bands and makes a list of their top tracks. Unlike MixtUp, this gives you a different path, Youtube links, and chooses a random top track.

## Usage
'''
bandlink [band1] [band2]
'''

## Example
'''
bandlink "R.E.M." "Queen"
R.E.M. - Man On The Moon
(https://www.youtube.com/watch?v=AW-66e_wyxg)
U2 - Beautiful Day
(https://www.youtube.com/watch?v=co6WMzDOh1o)
Queen - We Will Rock You - Remastered 2011
(https://www.youtube.com/watch?v=BPUzsg5UsjM)

Playlist: http://www.youtube.com/watch_videos?video_ids=AW-66e_wyxg,co6WMzDOh1o,BPUzsg5UsjM
'''

## TODO
- [ ] Format code and more documentation
- [ ] A* with genre as a heuristic
- [ ] Use a database or something to save data
- [ ] Cool UI?!
