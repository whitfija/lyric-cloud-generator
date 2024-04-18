# imports
from flask import render_template, request
from app import app
from .lyrics_processing.processor import process_lyrics

# home
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Album Wordcloud Generator')

# wordcloud
@app.route('/wordcloud', methods=['POST'])
def wordcloud():
    # form data
    album = request.form['album']
    artist = request.form['artist']

    # process
    processed_data = process_lyrics(album, artist)
    wordcloud_image = processed_data['wordcloud_image']

    # display page
    return render_template('wordcloud.html', title='Wordcloud', wordcloud_image=wordcloud_image)