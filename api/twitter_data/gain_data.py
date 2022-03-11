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
from spotipy_section.graphPlaylist import label_heatmap, get_artist_song_name
from twitter_data import innit_tweepy

tweepy_api = innit_tweepy.get_tweepy_api()

CHOICE = '"open.spotify.com/track" lang:en exclude:replies -filter:retweets'
song_list = []
user_screen_name_list = []
all_tweets = []

TWEET_COLUMN__NAMES = ["user_name", "text", "track_id", "tweet_id", "time"]
all_s_tweets = pd.DataFrame(columns=TWEET_COLUMN__NAMES)

# Defined in sentiment_analyser.py
label_df = pd.DataFrame(columns=COLUMN_HEADINGS)

BLACKLIST = ['BBC3MusicBot', 'BBCR6MusicBot', 'BBC2MusicBot', 'KiddysplaceMx', 'Spotweefy', 'JohnOxley777',
             'bieberonspotify',
             'LiveMixPlay', 'CAA_Official', 'fabclaxton', 'THXJRT', 'moevazquez']

NUM_USERS = 10
MAX_SONG_TWEETS = 50
NUM_BEFORE_TWEETS = 3
S_TWEET_MIN_NUM = 6

FILE_NAME = 'twitter_data/user_s_tweet_data.csv'
CHOSEN_USER = ""

# Gets recent tweets which include spotify links,  .items(n) -> how many different users will be searched
recent_s_tweets = tweepy.Cursor(tweepy_api.search_tweets, q=CHOICE, result_type='recent').items(NUM_USERS)

# Saved for reuse - helpful for web application
predictor = Prediction


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


# Adds to pre-defined list of users, the usernames from tweets
def init_user_list():
    """
    The method that creates that populates a list with user screen names.

    """
    for tweet in recent_s_tweets:
        user_screen_name_list.append(tweet.user.screen_name)


# Gets only spotify tweets from a user - passed as string
def get_user_s_tweets(screen_name):
    """
    The function that returns filtered/queried tweets from a user.

    :param str screen_name: The screen name of a user.
    :return: Queried tweets from the user (based on most recent tweets)
    
    """
    query = '"open.spotify.com/track" lang:en exclude:replies -filter:retweets' + " from:" + screen_name
    # Gets specified number of tweets that include songs in the tweets
    spotify_tweets = tweepy.Cursor(tweepy_api.search_tweets, q=query, result_type='recent').items(MAX_SONG_TWEETS)
    return spotify_tweets


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


# Gets tweet message and song url (if there is one)
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


# Puts passed data into dataframe
def tabulate_s_tweets(user_name, text, track_id, tweet_id, time):
    """
    The method that generates a dataframe for user data.

    :param user_name: The users screen name.
    :param text: The text from the tweet.
    :param track_id: The track id from the tweet.
    :param tweet_id: The tweet id.
    :param time: The time of the tweet.

    """
    df = {'user_name': user_name, 'text': text, 'track_id': track_id, 'tweet_id': tweet_id, 'time': time}
    global all_s_tweets
    all_s_tweets = all_s_tweets.append(df, ignore_index=True)


# Creates a song list for each user from the dataframe (all_s_tweets)
# TODO check return on this function
def get_users_song_lists():
    """
    The function that returns a list of track lists for each user from the dataframe 'all_s_tweets'.

    :return: a list of track lists per user.
    :rtype: list[list[str]]
    """
    all_user_lists = []
    # iterates through each user within s_tweets
    for user in all_s_tweets['user_name'].unique():
        user_song_list = []
        for row in all_s_tweets[all_s_tweets['user_name'] == user].iterrows():
            # Gets track ID from tweet
            # Checks for no track (and for when it reads data from csv - empty is stored as float
            if row[1][2] != "" and type(row[1][2]) == str:
                user_song_list.append(row[1][2])

        if user_song_list:
            all_user_lists.append(user_song_list)
    return all_user_lists


# Adds the sentiment label to each song in the dataframe
def add_song_label(messages):
    """
    The method that adds the sentiment for a tweet.

    :param messages: Messages from current tweet and past tweets.

    """
    global label_df

    label = get_text_senti(messages)
    try:
        label = label.to_frame().T
        label_df = label_df.append(label, ignore_index=True)
    except AttributeError:
        label_df = label_df.append(pd.Series(0, index=label_df.columns), ignore_index=True)


# Gets the averaged sentiment of each song tweet from previous tweets
def get_before_s_tweets():
    """
    The method that gets previous tweets per tweet in 'all_s_tweets' and assigns the sentiment label per track.

    """
    # example_user = all_s_tweets.iloc[0]

    # For each user in the dataframe
    for user in all_s_tweets['user_name'].unique():
        print(user, ": ")
        # For each spotify tweet that user has made
        for s_tweet in all_s_tweets[all_s_tweets['user_name'] == user].iterrows():
            messages = ""

            # Gets date (YYY-MM-DD) of tweet - use to limit tweets only going back 7 days - only to keep tweets
            # within bound
            until_date = s_tweet[1][4].date()

            # Increments 1 to account for the current tweet
            until_date += timedelta(days=1)

            # Gets tweet_id
            tweet_id = int64(s_tweet[1][3])

            # Query for tweets from user
            query = 'lang:en exclude:replies -filter:retweets ' + user

            # Gets (upto number declared) tweets from user - until: searches tweets BEFORE given date
            before_s_tweet = tweepy.Cursor(tweepy_api.search_tweets,
                                           q=query,
                                           result_type='recent',
                                           max_id=tweet_id,
                                           until=until_date
                                           ).items(NUM_BEFORE_TWEETS)
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
            add_song_label(messages)


# Remove any blacklisted accounts
def rem_blacklist():
    """
    The method that removes blacklisted accounts from the 'user_screen_name_list'.

    """
    for user_name in BLACKLIST:
        try:
            user_screen_name_list.remove(user_name)
        except ValueError:
            pass


# Creates the dataframe of songs and other data for either a chosen user or if none, a selection of random users
def create_s_tweet_df(chosen_user):
    """
    The method that creates a dataframe of spotify tweets.
    Can be for just one user if specified, otherwise uses a group of random users (based on recent activity).

    :param chosen_user: (Optional) Only create for a specific user by screen name.

    """
    global all_s_tweets
    global CHOSEN_USER
    if chosen_user:
        CHOSEN_USER = chosen_user
        get_s_tweet(chosen_user)
    else:
        # Creates list of users who have posted using a spotify link in their tweet
        init_user_list()
        # Removes users on blacklist
        rem_blacklist()
        for user in user_screen_name_list:
            # If there are more than 2 tweets that the user has made which includes a spotify track, (DIS-COUNTS USERS
            # WITH LESS - hence not always selected number of users shown in table
            get_s_tweet(user)


# Strange error where the call to get_user_s_tweets cannot be stored
def get_s_tweet(user):
    """
    The method that tabulate spotify tweets for a random collective or a given user.

    :param user: (Optional) A specific user screen name

    """
    global all_s_tweets
    if count_iterable(get_user_s_tweets(user)) > S_TWEET_MIN_NUM:
        # For each tweet, extract each component and collate it in a dataframe
        for tweet in get_user_s_tweets(user):
            text, track_id = get_s_tweet_text_and_track_id(tweet)
            if track_id != "":
                tabulate_s_tweets(user_name=user, text=text, track_id=track_id, tweet_id=tweet.id,
                                  time=tweet.created_at)


# Reads in a file to the main all_s_tweets dataframe
def read_s_tweet_file(file_name):
    """
    The method that reads in a saved CSV file ('user_s_tweet_data.csv') into all_s_tweet.

    :param file_name: A specified file to read into

    """
    global all_s_tweets
    dtypes = {'user_name': 'str', 'text': 'str', 'track_id': 'str', 'tweet_id': 'int64', 'time': 'str'}
    parse_date = ['time']
    all_s_tweets = pd.read_csv(file_name, index_col=0, dtype=dtypes, parse_dates=parse_date)
    all_s_tweets["track_id"].astype(str)
    all_s_tweets.dropna(subset=["track_id"], inplace=True)


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
                lyric_df = lyric_df.append(pd.Series(dtype=float), ignore_index=True)
            else:
                lyric_df = lyric_df.append(row, ignore_index=True)
        except AttributeError:
            lyric_df = lyric_df.append(pd.Series(dtype=float), ignore_index=True)
    lyric_df.reset_index(inplace=True, drop=True)
    lyric_df = lyric_df.fillna(0)
    df_concat = pd.concat([df, lyric_df], axis=1)
    return df_concat


#
def get_heatmap():
    """
    The function that produces a 3D interpolation graph for each emotion using 'energy' and 'valence' as axis

    """
    data_to_graph = all_s_tweets
    data_to_graph = (data_to_graph[data_to_graph['anger'].notna()])
    mode_user_name = data_to_graph['user_name'].value_counts().idxmax()
    data_to_graph = data_to_graph.loc[data_to_graph['user_name'] == mode_user_name]
    data_to_graph = data_to_graph.reset_index().drop(columns='index')
    data_to_graph = data_to_graph.drop(columns=['text', 'tweet_id', 'time'])
    label_heatmap(data_to_graph)


# Classifies the data and uses a predicting model
def classify_data():
    """
    The function that formats data and generates the classification models and returns the predicted values for
    recently listened to songs. (The return value is designed as the first application of classification is for
    recently played music on web application).

    :return: The predicted sentiment values for each emotion for each recently listened to song.

    """
    global predictor
    data_to_graph = all_s_tweets
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

    # Linear models for joy
    # classifier = LinLogReg(data_to_graph, "joy")
    # classifier.classify()

    # SVM for joy
    # svm_classify = KernelSVC(data_to_graph, "joy")
    # svm_classify.predict_recent_songs()

    # KNR for joy and sadness
    predictor = Prediction(data_to_graph)
    return predictor.predict_recent_songs()

    # print('sadness')
    # knr_joy = KNeighborRegressor(data_to_graph, "sadness")
    # knr_joy.predict_recent_songs()

    # print('anger')
    # knr_joy = KNeighborRegressor(data_to_graph, "anger")
    # knr_joy.predict_recent_songs()


# Gets the longest song song list from all users
def get_max_song_list():
    """
    The function that return the largest song list from all user track lists.

    :return: Largest track list.
    :rtype: list
    """
    # gets all users song lists
    all_song_lists = get_users_song_lists()
    # Gets the largest list of songs
    return max(x for x in all_song_lists)


# Trawls twitter for data on either a specific user or a random selection
def trawl_data(screen_name):
    """
    The driver method for mining new data from twitter.

    :param screen_name: (Optional) Only mine data for a specific user.

    """
    global all_s_tweets
    global label_df
    # Creates df of tweet data
    create_s_tweet_df(screen_name)
    # Gets a couple of previous tweets from a user before they posted a specific song
    get_before_s_tweets()
    # Also adds labels of sentiment to each song
    all_s_tweets = pd.concat([all_s_tweets, label_df], axis=1)
    # Saves data into csv
    all_s_tweets.to_csv(FILE_NAME)
    # get_heatmap()


# Loads the data
def load_data():
    """
    The driver method for loading data from a csv file.

    """
    # read_s_tweet_file("data/user_s_tweet_data.csv")
    read_s_tweet_file(FILE_NAME)


def _main_():
    """
    The driver function that runs necessary functions for web application to operate

    :return: The sentiment prediction for recently played song.
    """
    print("run")
    global all_s_tweets
    global label_df

    # Gets new data from twitter and also saves into csv
    # trawl_data("kwangyajail")
    # Displays whole table of all users and corresponding spotify tweets
    # display(all_s_tweets)

    # Open csv and put into s_tweetsd
    read_s_tweet_file(FILE_NAME)

    # Gets the largest list of songs
    # max_list = get_max_song_list()

    # Graphs the largest song list
    # graph_one_playlist(max_list)

    # get_heatmap()
    return classify_data()


def predict_searched_song(track_id):
    """
    The function that gets the sentiment prediction for a single track.

    :param str track_id: The track id of the desired track.
    :return: The sentiment for each emotion of the track.

    """
    global predictor
    return predictor.predict_this_song(track_id)