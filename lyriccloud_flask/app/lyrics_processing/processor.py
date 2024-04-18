from lyricsgenius import Genius
from .storm_topology import SimpleTopology
import json

def get_genius_token():
    with open('config.json', 'r') as f:
        config = json.load(f)
        return config.get('genius_token')
    
genius = Genius(get_genius_token())

def process_lyrics(albumtitle, artist):
    # get all albums lyrics
    album = genius.search_album(albumtitle, artist)
    tracks = album.tracks
    song_lyrics = []

    # separate tracks
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

    # lyrics_list is now a list of strings

    # none found
    if not lyrics_list:
        return {"error": "No lyrics found for the specified album and artist."}

    # apache storm
    # initialize topology
    topology = SimpleTopology()

    # run the topology
    processed_data = topology.run(lyrics_list)
    
    processed_data = {  }
    return processed_data