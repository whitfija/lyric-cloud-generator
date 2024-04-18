from lyricsgenius import Genius
#from storm_topology import SimpleTopology
import json
import os
from wordcloud import WordCloud
import io
import base64
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, concat_ws
from pyspark.sql.types import ArrayType, StringType

def get_genius_token():
    current_directory = os.getcwd()
    print("Current directory:", current_directory)
    with open('app\lyrics_processing\config.json', 'r') as f:
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
                lyrics_content = lyrics_content.split("Embed", 1)[0].strip()
                lyrics_content = lyrics_content.split("1Embed", 1)[0].strip()
                lyrics_content = lyrics_content.split("You might also likeEmbed", 1)[0].strip()
                
                # add if not empty
                if lyrics_content:
                    lyrics_list.append(lyrics_content)

    # lyrics_list is now a list of strings

    # none found
    if not lyrics_list:
        return {"error": "No lyrics found for the specified album and artist."}
    
    word_list = combine_words_from_strings(lyrics_list)

    # spark processing

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("LyricsWordCloud") \
        .getOrCreate()

    # Create a DataFrame with a single column containing the word_list
    df = spark.createDataFrame([(word_list,)], ["words"])

     # Convert the words column to a string by concatenating all elements with a space separator
    df = df.withColumn("words_str", concat_ws(" ", "words"))

    # Explode the words_str column to split words into rows
    df_exploded = df.select(explode(split(col("words_str"), " ")).alias("word"))

    # Group by word and count occurrences
    word_counts = df_exploded.groupBy("word").count()

    # Order by count in descending order to get the most common words
    top_100_words = word_counts.orderBy(col("count").desc()).limit(100)

    # Collect the top 100 words as a list
    top_100_words_list = top_100_words.select("word").rdd.flatMap(lambda x: x).collect()

    # Split the processing by songs and combine the results into the word_list
    # You can implement this part based on your specific needs and the structure of your data

    #print(top_100_words_list)

    # Stop Spark session
    spark.stop()

    final_words = ' '.join(top_100_words_list)
    print(final_words)

    # build word cloud
    wordcloud = WordCloud(width = 800, height = 800,
                background_color="rgba(255, 255, 255, 0)", mode="RGBA",
                stopwords = ['supercalifragilisticexp'],
                min_font_size = 10).generate(final_words)
    img_buffer = io.BytesIO()
    wordcloud.to_image().save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    return {"wordcloud_image": img_str}

def combine_words_from_strings(string_list):
        all_words = []
        for string in string_list:
            words = string.split()
            all_words.extend(words)
        return all_words