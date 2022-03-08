from matplotlib import pyplot as plt
import numpy as np

from classification.classification import KNeighborRegressor, DecisionTree
from spotipy_section.graphPlaylist import get_song_list_ids, get_all_music_features, get_recently_played, \
    get_artist_song_name

# track_list = get_song_list_ids('7d6WFDrKCCz4veVu0p7PVt')

# Only runs once when server starts, needs to be updated when login/logout
# song_name, track_list = get_recently_played()


# An object containing the model, scalar and pca used to fit the specified emotion
class EmotionModel:
    """
    A class that creates an instance of prediction models for a given emotion.

    Attributes:
        str emotion: The chosen type of emotion to train the model by.
        data_to_graph: The user data and labels required to train the model.

    """
    def __init__(self, emotion, data_to_graph):
        """
        The constructor for the EmotionModel class.

        :param str emotion: The chosen type of emotion to train the model by.
        :param data_to_graph: The user data and labels required to train the model.
        """
        self.emotion = emotion
        # self.model, self.scalar, self.pca = KNeighborRegressor(data_to_graph, emotion).predict_recent_songs()
        self.model, self.scalar, self.pca = DecisionTree(data_to_graph, emotion).drive()

    # Makes predictions for a chosen list of tracks
    def predict(self, track_list):
        """
        The function that predicts the sentiment for a given list of tracks.

        :param list track_list: the list of tracks to predict.
        :return: sentiment prediction per track.

        """
        return self.model.predict(get_playlist_data(self, track_list))

    def predict_song(self, track_id):
        """
        The function that only predicts a single track.

        :param str track_id: the trackid.
        :return: The predicted value based on the model.
        """
        return self.model.predict(get_playlist_data(self, [track_id]))


# Gets prepared data from playlist in this method
def get_playlist_data(emotion_model, track_list):
    """
    The function that prepares the data according to the model gets the musical features of each track.

    :param emotion_model: The selected model being used.
    :param list track_list: The list of track ids.
    :return: Data to be predicted for sentiment by model.

    """
    # track_list = get_song_list_ids('7d6WFDrKCCz4veVu0p7PVt')
    tracks_features = get_all_music_features(track_list)

    tracks_features = emotion_model.scalar.transform(tracks_features)
    predict_playlist_data = emotion_model.pca.transform(tracks_features)
    return predict_playlist_data


class Prediction:
    """
    A class that instantiates instances of EmotionModel for each emotion.

    Attributes:
        data_to_graph: User data required to create the model for prediction.

    """
    def __init__(self, data_to_graph):
        """
        The constructor for the class Prediction

        :param  data_to_graph: User data required to create the model for prediction.

        """
        self.anger = EmotionModel("anger", data_to_graph)
        self.fear = EmotionModel("fear", data_to_graph)
        self.joy = EmotionModel("joy", data_to_graph)
        self.sadness = EmotionModel("sadness", data_to_graph)

    anger_pred = []
    fear_pred = []
    joy_pred = []
    sadness_pred = []

    song_anger_pred = []
    song_fear_pred = []
    song_joy_pred = []
    song_sadness_pred = []

    def predict_recent_songs(self):
        """
        The function that predicts sentiments for each emotion for a list of recently listened to tracks.

        :return: A list of sentiments per emotion for recently listened to tracks (ascending time listened to).
        :rtype: list[float]
        """
        recent_track_list = get_recently_played()

        self.anger_pred = self.anger.predict(recent_track_list)[::-1]
        self.fear_pred = self.fear.predict(recent_track_list)[::-1]
        self.joy_pred = self.joy.predict(recent_track_list)[::-1]
        self.sadness_pred = self.sadness.predict(recent_track_list)[::-1]
        # self.graph()
        return self.anger_pred.tolist(), self.fear_pred.tolist(), self.joy_pred.tolist(), self.sadness_pred.tolist()

    def predict_this_song(self, track_id):
        """
        The function that predicts the sentiment for each emotion of a single track.

        :param track_id: The track id of the chosen song.
        :return: A list of sentiment per emotion for the given track.
        :rtype: list[float]

        """
        self.song_anger_pred = self.anger.predict_song(track_id)
        self.song_fear_pred = self.fear.predict_song(track_id)
        self.song_joy_pred = self.joy.predict_song(track_id)
        self.song_sadness_pred = self.sadness.predict_song(track_id)
        return self.song_anger_pred.tolist(), self.song_fear_pred.tolist(), self.song_joy_pred.tolist(), self.song_sadness_pred.tolist()

    def graph(self):
        """
        The method that graphs teh predicted sentiment.

        """
        recent_track_list = ["FIll this in to produce matplotlib graph"]
        x = range(1, len(recent_track_list) + 1)
        j, f, a, s = map(list, zip(*sorted(zip(self.joy_pred, self.fear_pred, self.anger_pred, self.sadness_pred))))
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(x, a, label="Anger", c='r')
        ax.plot(x, f, label="Fear", c='m')
        ax.plot(x, j, label="Joy", c='y')
        ax.plot(x, s, label="Sadness", c='b')
        plt.legend()
        plt.ylim(0, 1)
        plt.show()
