from lyricsgenius import Genius

token = '[]'

genius = Genius(token)
#artist = genius.search_artist("Kendrick Lamar", max_songs=3, sort="title")
# print(artist.songs)

# Way 1
#song = genius.search_song("Momma", artist.name)

# Way 2
# this will search artist.songs first
# and if not found, uses search_song
#song = artist.song("Momma")

#print(type(song))
#print(type(song.lyrics))

album = genius.search_album("Thousands of Evils", "Vildhjarta")
print(album)