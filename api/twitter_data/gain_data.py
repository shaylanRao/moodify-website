import re
from datetime import timedelta
from string import punctuation

import pandas as pd
import tweepy
# from IPython.core.display import display
from numpy import int64

from classification.senti_prediciton import Prediction
from sentiment.lyric_sentiment import get_lyrics_senti
from sentiment.sentiment_analyser import get_text_senti, COLUMN_HEADINGS
from spotipy_section.graphPlaylist import get_artist_song_name
from twitter_data import innit_tweepy


# Gets tweet message and song url (if there is one)
def get_trackid_from_urls(urls):
    """
    The function that returns the trackid from a spotify track URL.

    :param urls: A spotify track URL.
    :return: The corresponding track id.
    :rtype: str

    """
    try:
        url = urls[0]['expanded_url']
    except (IndexError, KeyError):
        url = ""

    if url[0:31] == "https://open.spotify.com/track/" and len(url) == 100:
        url = (url[31:53])
        return url

    return ""


# Cleans text data - passed as string
def clean_text(message):
    """
    The function that cleans the tweet texts.

    :param message: The tweet message.
    :return: The cleaned tweet message. (can be processed for sentiment and saved in dataframe).
    :rtype: str

    """
    try:
        # Removes space, flattens text
        tweet_text = message.replace('\n', ' ')

        # Removes urls
        tweet_text = re.sub(r'http\S+', '', tweet_text)

        # Removes any 'special' characters
        tweet_text = re.sub("[^0-9a-zA-Z{} ]+".format(punctuation), "", tweet_text)
    except AttributeError:
        print("ATTRIBUTE ERROR in clean_text")
        return ""

    return tweet_text


def get_s_tweet_text_and_track_id(tweet):
    """
    The function that obtains the track URL and the clean message from a tweet.

    :param tweet: The tweet object.
    :return: tweet text, track id.
    :rtype: str

    """
    tweet_text = clean_text(tweet.text)
    urls = tweet.entities["urls"]
    song_url = get_trackid_from_urls(urls)
    return tweet_text, song_url


# Function for counting number of elements, solves bug - unable to do for each for some object types
def count_iterable(i):
    """
    The function that counts how many items are in an object.
    Designed to overcome bug of not being able to iterate some objects.

    :param i: object to count elements in.
    :return: number of items in object.
    :rtype: integer

    """
    return sum(1 for _ in i)


# Gets the sentiment analysis on each song
def get_lyric_sentiment(df):
    """
    The function that gets and appends lyric sentiment

    :param df: The dataframe containing track ids (from 'data_to_graph' ideally but any dataframe)

    :return: The dataframe with lyrical sentiment appended

    """
    lyric_df = pd.DataFrame()
    for row_index, df_row in df.iterrows():
        trackid = df_row['track_id']
        song_name, artist_name = get_artist_song_name(trackid)
        row = get_lyrics_senti(song_name, artist_name)
        try:
            if row.empty:
                lyric_df = pd.concat([lyric_df, pd.Series(dtype=float)], ignore_index=True, axis=0)
            else:
                lyric_df = pd.concat([lyric_df, row], ignore_index=True, axis=0)
        except AttributeError:
            lyric_df = pd.concat([lyric_df, pd.Series(dtype=float)], ignore_index=True, axis=0)
    lyric_df.reset_index(inplace=True, drop=True)
    lyric_df = lyric_df.fillna(0)
    df_concat = pd.concat([df, lyric_df], axis=1)
    return df_concat


class GainData:
    def __init__(self, user_screen_name):
        """
        The constructor for the EmotionModel class.

        :param user_screen_name: The users screen name on twitter
        """
        self.tweet_column_names = ["user_name", "text", "track_id", "tweet_id", "time"]

        self.user_screen_name = user_screen_name
        self.all_s_tweets = pd.DataFrame(columns=self.tweet_column_names)
        self.label_df = pd.DataFrame(columns=COLUMN_HEADINGS)
        # Saved for reuse - helpful for web application
        self.predictor = Prediction
        self.tweepy_api = innit_tweepy.get_tweepy_api()
        self.CHOICE = '"open.spotify.com/track" lang:en exclude:replies -filter:retweets'
        self.song_list = []
        self.all_tweets = []
        self.MAX_SONG_TWEETS = 50
        self.NUM_BEFORE_TWEETS = 3
        self.S_TWEET_MIN_NUM = 6
        self.FILE_NAME = 'twitter_data/user_s_tweet_data.csv'
        self.SAVE_TEMP_DATA_FILE_NAME = 'twitter_data/new_trawl_user_data.csv'

    # Gets only spotify tweets from the user - passed as string
    def get_user_s_tweets(self):
        """
        The function that returns filtered/queried tweets from the user.

        :return: Queried tweets from the user (based on most recent tweets)

        """
        query = '"open.spotify.com/track" lang:en exclude:replies -filter:retweets' + " from:" + self.user_screen_name
        # Gets specified number of tweets that include songs in the tweets
        spotify_tweets = tweepy.Cursor(self.tweepy_api.search_tweets, q=query, result_type='recent').items(
            self.MAX_SONG_TWEETS)
        return spotify_tweets

    # Puts passed data into dataframe
    def tabulate_s_tweets(self, text, track_id, tweet_id, time):
        """
        The method that generates a dataframe for user data.

        :param text: The text from the tweet.
        :param track_id: The track id from the tweet.
        :param tweet_id: The tweet id.
        :param time: The time of the tweet.

        """
        df = pd.DataFrame([[self.user_screen_name, text, track_id, tweet_id, time]], columns=self.tweet_column_names)

        self.all_s_tweets = pd.concat([self.all_s_tweets, df], ignore_index=True, axis=0)

    def get_user_song_list(self):
        """
        The function that returns a list of tracks from the dataframe 'all_s_tweets'.

        :return: a list of track lists per user.
        :rtype: list[list[str]]
        """

        user_song_list = []
        for row in self.all_s_tweets.iterrows():
            # Gets track ID from tweet
            # Checks for no track (and for when it reads data from csv - empty is stored as float
            if row[1][2] != "" and type(row[1][2]) == str:
                user_song_list.append(row[1][2])

        return user_song_list

    # Adds the sentiment label to each song in the dataframe
    def add_song_label(self, messages):
        """
        The method that adds the sentiment for a tweet.

        :param messages: Messages from current tweet and past tweets.

        """
        label = get_text_senti(messages)
        try:
            label = label.to_frame().T
            self.label_df = pd.concat([self.label_df, label], ignore_index=True, axis=0)
        except AttributeError:
            self.label_df = pd.concat([self.label_df, pd.Series(0, index=self.label_df.columns)],
                                      ignore_index=True,
                                      axis=0)

    # Gets the averaged sentiment of each song tweet from previous tweets
    def get_before_s_tweets(self):
        """
        The method that gets previous tweets per tweet in 'all_s_tweets' and assigns the sentiment label per track.

        """
        print(self.user_screen_name, ": ")
        # For each spotify tweet that user has made
        for s_tweet in self.all_s_tweets.iterrows():
            messages = ""

            # Gets date (YYY-MM-DD) of tweet - use to limit tweets only going back 7 days - only to keep tweets
            # within bound
            until_date = s_tweet[1][4].date()

            # Increments 1 to account for the current tweet
            until_date += timedelta(days=1)

            # Gets tweet_id
            tweet_id = int64(s_tweet[1][3])

            # Query for tweets from user
            query = 'lang:en exclude:replies -filter:retweets ' + self.user_screen_name

            # Gets (upto number declared) tweets from user - until: searches tweets BEFORE given date
            before_s_tweet = tweepy.Cursor(self.tweepy_api.search_tweets,
                                           q=query,
                                           result_type='recent',
                                           max_id=tweet_id,
                                           until=until_date
                                           ).items(self.NUM_BEFORE_TWEETS)
            for tweet in before_s_tweet:
                # If the tweet is not the spotify tweet
                if tweet.id != tweet_id:
                    # And does not have any other spotify song associated with it
                    if get_trackid_from_urls(tweet.entities["urls"]) == "":
                        messages = '\n'.join([messages, clean_text(tweet.text)])
                    else:
                        # Go to next tweet
                        break
                else:
                    messages = '\n'.join([messages, clean_text(tweet.text)])

            # Gets overall sentiment from past tweets together (rounded sentiment leading upto song)
            #     Acts as label for song
            self.add_song_label(messages)

    # Strange error where the call to get_user_s_tweets cannot be stored (hence same call function twice)
    def get_s_tweet(self):
        """
        The method that tabulate spotify tweets for the user.

        """
        if count_iterable(self.get_user_s_tweets()) > self.S_TWEET_MIN_NUM:
            # For each tweet, extract each component and collate it in a dataframe
            for tweet in self.get_user_s_tweets():
                text, track_id = get_s_tweet_text_and_track_id(tweet)
                if track_id != "":
                    self.tabulate_s_tweets(text=text, track_id=track_id,
                                           tweet_id=tweet.id,
                                           time=tweet.created_at)
        else:
            return "NOT ENOUGH!"

    # Reads in a file to the main all_s_tweets dataframe
    def read_s_tweet_file(self):
        """
        The method that reads in a saved CSV file ('user_s_tweet_data.csv') into all_s_tweet.

        """
        dtypes = {'user_name': 'str', 'text': 'str', 'track_id': 'str', 'tweet_id': 'int64', 'time': 'str'}
        parse_date = ['time']
        new_data = pd.read_csv(self.SAVE_TEMP_DATA_FILE_NAME, index_col=0, dtype=dtypes, parse_dates=parse_date)
        new_data["track_id"].astype(str)
        saved_data = pd.read_csv(self.FILE_NAME, index_col=0, dtype=dtypes, parse_dates=parse_date)
        saved_data["track_id"].astype(str)

        # Merge new data into existing data
        self.all_s_tweets = pd.concat([new_data, saved_data], axis=0)

        self.all_s_tweets = self.all_s_tweets.drop_duplicates()
        self.all_s_tweets = self.all_s_tweets.reset_index(drop=True)

        # Save merged data into file to load for future
        self.all_s_tweets.to_csv(self.FILE_NAME)
        self.all_s_tweets.dropna(subset=["track_id"], inplace=True)

    # Classifies the data and uses a predicting model
    def classify_data(self):
        """
        The function that formats data and generates the classification models and returns the predicted values for
        recently listened to songs. (The return value is designed as the first application of classification is for
        recently played music on web application).

        :return: The predicted sentiment values for each emotion for each recently listened to song.

        """
        data_to_graph = self.all_s_tweets
        # If a row has all values N/A, anger would contain N/A, this code removes any rows with N/A for all values
        data_to_graph = (data_to_graph[data_to_graph['anger'].notna()])
        # Removes rows which show no emotion
        data_to_graph = data_to_graph.drop(data_to_graph[(data_to_graph.anger == 0) & (data_to_graph.fear == 0) & (
                data_to_graph.joy == 0) & (data_to_graph.sadness == 0)].index)
        # Gets the user with the most records
        mode_user_name = data_to_graph['user_name'].value_counts().idxmax()
        # Forms array of same (mode) user data
        data_to_graph = data_to_graph.loc[data_to_graph['user_name'] == mode_user_name]
        # Selects relevant columns
        data_to_graph = data_to_graph.reset_index().drop(columns=['index', 'text', 'tweet_id', 'time'])
        # display(data_to_graph)

        # Get lyrical data
        # data_to_graph = get_lyric_sentiment(data_to_graph)

        # Saves data to csv
        data_to_graph.to_csv('datatoclassify.csv')

        print(mode_user_name, "'s ", "Data Size: ", len(data_to_graph))

        self.predictor = Prediction(data_to_graph)
        return self.predictor.predict_recent_songs()

    # Trawls twitter for data on either a specific user or a random selection
    def trawl_data(self):
        """
        The driver method for mining new data from twitter.

        """
        # Creates df of tweet data
        self.get_s_tweet()
        # Gets a couple of previous tweets from a user before they posted a specific song
        self.get_before_s_tweets()
        # Also adds labels of sentiment to each song
        self.all_s_tweets = pd.concat([self.all_s_tweets, self.label_df], axis=1)
        # Saves data into csv
        self.all_s_tweets.to_csv(self.SAVE_TEMP_DATA_FILE_NAME)

    # DRIVER FUNCTION
    def populate_and_classify(self):
        """
        The driver function that runs necessary functions for web application to operate

        :return: The sentiment prediction for recently played song.
        """
        print("run")

        # Gets new data from twitter and also saves into csv
        self.trawl_data()
        # Displays whole table of all users and corresponding spotify tweets
        # display(all_s_tweets)

        # Open csv and put into s_tweets
        self.read_s_tweet_file()

        return self.classify_data()

    def predict_searched_song(self, track_id):
        """
        The function that gets the sentiment prediction for a single track.

        :param str track_id: The track id of the desired track.
        :return: The sentiment for each emotion of the track.

        """
        return self.predictor.predict_this_song(track_id)
