from lyricsgenius import Genius
import json

token = '3rMFou0uHqLaG3wSJFW--TcDJQ7Mn29zHzyHKIwq5p_nNVDusURiKm52trx2vzPfUTUOIGa5ME4qk6d4OEA84g'

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
tracks = album.tracks
song_lyrics = []

# Retrieve song information
for track in tracks:
    songinfo = json.loads(track.to_json())
    song_lyrics.append(songinfo)
    print('Song added')

# filter out entries with empty or missing lyrics
lyrics_list = []
for song in song_lyrics:
    if 'song' in song and 'lyrics' in song['song']:
        lyrics = song['song']['lyrics']
        # start collection after 'Lyrics'
        split_lyrics = lyrics.split("Lyrics", 1)
        if len(split_lyrics) > 1:
            lyrics_content = split_lyrics[1].strip()
            # remove extra stuff
            lyrics_content = lyrics_content.split("1Embed", 1)[0].strip()
            lyrics_content = lyrics_content.split("You might also likeEmbed", 1)[0].strip()
            
            # add if not empty
            if lyrics_content:
                lyrics_list.append(lyrics_content)

# print the lyrics list
for lyrics in lyrics_list:
    print("----------------------------")
    print(lyrics)