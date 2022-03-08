import requests
# from IPython.core.display import display
from bs4 import BeautifulSoup
import re
import unidecode

from sentiment.sentiment_analyser import get_lyr_senti


def get_lyrics_senti(song_name, artist_name):
    """
    The function that gets the sentiment values from text in lyrics.

    :param str song_name: The name of the song.
    :param str artist_name: The artist of the song.

    """
    song_name = clean_text(song_name)
    artist_name = clean_text(artist_name)
    page_name = 'https://genius.com/' + artist_name + '-' + song_name + '-' + 'lyrics'
    print(page_name)
    page = requests.get(page_name)
    soup = BeautifulSoup(page.content, 'lxml')
    lyrics = ""

    for tag in soup.select('div[class^="Lyrics__Container"], .song_body-lyrics p'):
        text = tag.get_text(strip=True, separator='\n')
        if text:
            lyrics += re.sub("[\(\[].*?[\)\]]", "", text)

    return get_lyr_senti(lyrics)


def clean_text(text):
    """
    The function that cleans the text for song name and artist.

    :param text: The string (song name, artist) required to be cleaned.
    :return: The clean string (to be used in url).
    :rtype: str

    """

    text = text.replace(" ", "-")
    text = text.replace("'", "")
    text = re.sub("[\(\[].*?[\)\]]", "", text)
    text = re.sub(r'-$', '', text)
    text = unidecode.unidecode(text)
    return text.lower()
