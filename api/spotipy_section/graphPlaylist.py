import matplotlib.pyplot as plt
import pandas as pd
import sklearn
import spotipy
# importing required libraries
from IPython.core.display import display
from pylab import *
from scipy.interpolate import griddata
from sklearn import manifold
from spotipy.oauth2 import SpotifyOAuth

SCOPE = "user-read-recently-played playlist-read-private"
CLIENT_ID = 'ed61ad2eb1ac48f38a5971328cec9f01'
CLIENT_SECRET = '3977cda8a7a14e63b5bdf985c0a5b440'
REDIRECT_URL = 'http://localhost:8080'

ALL_FEATURE_LABELS = ['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                      'liveness', 'valence', 'tempo']

# ALL_FEATURE_LABELS = ['energy', 'valence']

# Define scope and link to app
scope = SCOPE
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET, scope=scope,
                                               redirect_uri=REDIRECT_URL, show_dialog=True))


def get_artist_song_name(trackid):
    """
    The function that receives a track id and returns the song name and artist.

    :param str trackid: The chosen track id.
    :return: The track name, The artist name.

    """
    track = sp.track(trackid)
    song_name = track['name']
    artist_name = track['artists'][0]['name']
    return song_name, artist_name


def get_attribute(all_features, select_feature):
    """
    The function that returns the chosen attributes given all of the song features.

    :param all_features: All the features from a given track.
    :param select_feature: The selected feature to obtain.
    :return: A list of the selected feature.

    """
    return [all_features[i][select_feature] for i in range(len(all_features))]


def get_song_list_ids(pl_id):
    offset = 0
    response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,total',
                                 additional_types=['track'])
    song_list_ids = []
    for song in (response['items']):
        song_list_ids.append(song['track']['id'])
    # Removes any tracks that don't exist anymore
    song_list_ids = list(filter(None, song_list_ids))
    return song_list_ids


def get_w_to_z(song_list_ids, varw, varx, vary, varz):
    """
    The function that gets the attributes for 4 dimensions for a list of songs.

    :param song_list_ids: A list of track ids
    :param str varw: a desired feature.
    :param str varx: a desired feature.
    :param str vary: a desired feature.
    :param str varz: a desired feature.
    :return: 4 lists of features.
    :rtype list
    """
    # Get features for each song in list
    features = sp.audio_features(song_list_ids)
    features = list(filter(None, features))

    w = get_attribute(features, varw)
    y = get_attribute(features, vary)
    x = get_attribute(features, varx)
    z = get_attribute(features, varz)

    return w, x, y, z


def get_x_y_z(song_list_ids, varx, vary, varz):
    """
    The function that gets the attributes for 3 dimensions for a list of songs.

    :param song_list_ids:
    :param str varx: a desired feature.
    :param str vary: a desired feature.
    :param str varz: a desired feature.
    :return: 3 lists of features.
    :rtype: list

    """
    print(song_list_ids)
    # Get features for each song in list
    features = sp.audio_features(song_list_ids)
    # print(features[0])
    x = get_attribute(features, varx)
    y = get_attribute(features, vary)
    z = get_attribute(features, varz)

    return x, y, z


def get_all_music_features(song_list_ids):
    """
    The function that returns all music features given a list of track ids.

    :param song_list_ids: List of track ids.
    :return: A dataframe containing all features for corresponding tracks

    """
    features = sp.audio_features(song_list_ids)
    df = pd.DataFrame()
    for feature_label in ALL_FEATURE_LABELS:
        try:
            df[feature_label] = get_attribute(features, feature_label)
        except AttributeError:
            print("Track does not exist")

    return df


def show_graph_sample(varx, vary, varz, x1, x2, x3, y1, y2, y3, z1, z2, z3):
    """
    The method that produces a 3D graph of 3 features.

    :param str varx: A variable/feature.
    :param str vary: A variable/feature.
    :param str varz: A variable/feature.
    :param list x1: Corresponding values to the variable x.
    :param list x2: Corresponding values to the variable x.
    :param list x3: Corresponding values to the variable x.
    :param list y1: Corresponding values to the variable y.
    :param list y2: Corresponding values to the variable y.
    :param list y3: Corresponding values to the variable y.
    :param list z1: Corresponding values to the variable z.
    :param list z2: Corresponding values to the variable z.
    :param list z3: Corresponding values to the variable z.

    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(x1, y1, z1, c='y', marker='o')
    ax.scatter(x2, y2, z2, c='b', marker='o')
    ax.scatter(x3, y3, z3, c='r', marker='o')

    ax.set_xlabel(varx)
    ax.set_ylabel(vary)
    ax.set_zlabel(varz)

    plt.show()


def graph_one_playlist(song_list_graph_one, label):
    """
    The method that produces a graph for a list of tracks for 4 dimensions and can label points.

    :param song_list_graph_one: a track list of songs to graph.
    :param label: (Optional) labels for corresponding points.

    """
    print("GRAPH:")
    vw = 'acousticness'
    vx = 'valence'
    vy = 'energy'
    vz = 'speechiness'

    w, x, y, z = get_w_to_z(song_list_graph_one, vw, vx, vy, vz)
    # print(len(x))
    fig1 = plt.figure()

    ax = fig1.add_subplot(projection='3d', xlim=(0, 1), ylim=(0, 1), zlim=(0, 1))

    # 4-dimensions
    img = ax.scatter(x, y, z, c=w, cmap=plt.hot(), marker=".", edgecolors="black", linewidth=0.2, s=80)
    fig1.colorbar(img)

    # 3-dimensions
    # img = ax.scatter(x, y, z, marker=".")
    if label:
        for pointx, pointy, labelz in (zip(x, y, z)):
            if labelz > 0:
                ax.text(pointx, pointy, labelz, '%s' % (str(labelz)), size=5, zorder=1, c='red')
    counter = 0
    # for pointx, pointy, labelz in (zip(x, y, z)):
    #     ax.text(pointx, pointy, labelz, '%s' % (str(counter)), size=5, zorder=1, c='red')
    #     counter += 1

    ax.set_xlabel(vx)
    ax.set_ylabel(vy)
    ax.set_zlabel(vz)
    plt.show()


def get_recently_played():
    """
    The function that gets recently played tracks from the user.

    :return: A list of tracks.
    :rtype: list

    """
    results = sp.current_user_recently_played(limit=50)
    track_ids = []

    for idx, item in enumerate(results['items']):
        # track = item['track']
        # track_ids.append(item['track']['uri'])
        # time = item['played_at'].replace("T", "   ")
        # print(idx, item['track']['uri'], " – ", track['name'])
        # print(time)
        song_id = item['track']['uri'].split(":")
        track_ids.append(song_id[2])

    return track_ids


# -----------------------------------------------------------------------------

def label_heatmap(song_label_df):
    """
    The method that produces a 3D interpolation graph with labeled points for each 4 emotions.

    :param song_label_df: A dataframe (from gain_data.py) containing users, sentiment and track ids.

    """
    # Example user is the most common user
    example_user_name = str(song_label_df.user_name.mode()[0])
    # Reduces the df to only the chosen user
    song_label_df = song_label_df[song_label_df['user_name'] == example_user_name]

    song_label_df = song_label_df[song_label_df['anger'].notna()]
    track_list = song_label_df['track_id'].tolist()
    vx = 'valence'
    vy = 'energy'
    vz = 'speechiness'

    x, y, z = get_x_y_z(track_list, vx, vy, vz)

    # plotly_interpolation()

    # Define sentiment (label)
    attr1 = song_label_df['joy']
    # interpolation_grid(x, y, label1, attr_name)

    attr2 = song_label_df['sadness']
    # interpolation_grid(x, y, label2, attr_name)

    attr3 = song_label_df['fear']

    attr4 = song_label_df['anger']


    # interpolation_grid_2(x, y, [attr1, attr2], [vx, vy, 'emotion intensity1'])

    # vx = 'acousticness'
    # vy = 'liveness'
    # vz = 'speechiness'

    x, y, z = get_x_y_z(track_list, vx, vy, vz)

    # Gets grid data for both atttributes
    # interpolation_grid_2(x, y, [attr1, attr2], [vx, vy, 'emotion intensity'])

    # Gets two graph for each attribute
    interpolation_grid(x, y, attr1, [vx, vy, 'emotion intensity'], 'joy')
    interpolation_grid(x, y, attr2, [vx, vy, 'emotion intensity'], 'sadness')
    interpolation_grid(x, y, attr3, [vx, vy, 'emotion intensity2'], 'fear')
    interpolation_grid(x, y, attr4, [vx, vy, 'emotion intensity2'], 'anger')
    # grid_x, grid_y, grid_z = get_grids(x, y, attr1)
    # plotly_interpolation(grid_z)

    # test_graph(song_label_df)


def interpolation_grid(x, y, attr, label_name, title):
    """
    The function that generates a graph using a grid of points (variable plane)

    :param list x: A music feature list of values.
    :param list y: A music feature list of values.
    :param list attr: A sentiment attribute.
    :param str label_name: The name of the sentiment.
    :param str title: The title for the graph (Recommend using the sentiment label).
    """
    grid_x, grid_y, grid_z = get_grids(x, y, attr)

    fig = plt.figure()
    # ax = fig.gca(projection='3d')
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(grid_x, grid_y, grid_z, cmap=plt.cm.plasma)

    # Fixed label names for x and y

    ax.set_xlabel(label_name[0])
    ax.set_ylabel(label_name[1])
    ax.set_zlabel(label_name[2])

    ax.set_zlim(0, 1)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title(title)
    plt.show()


def interpolation_grid_2(x, y, attr, label_names):
    """
    REDUNDANT FUNCTION!
    The function that would have produced two grids together for different emotions.

    :param list x: A music feature list of values.
    :param list y: A music feature list of values.
    :param list attr: Sentiment attributes.
    :param str label_name: The name of the sentiment.
    :param str title: The title for the graph (Recommend using the sentiment label).

    """
    grid_x, grid_y, grid_z = get_grids(x, y, attr[0])
    print(grid_x)
    fig = plt.figure()
    # ax = fig.gca(projection='3d')
    ax = fig.add_subplot(projection='3d')

    ax.plot_surface(grid_x, grid_y, grid_z, cmap=plt.cm.plasma)

    for pointx, pointy, labelz in (zip(x, y, attr[0])):
        if labelz > 0:
            ax.text(pointx, pointy, labelz, '%s' % (str(labelz)), size=7, zorder=1, c='red')

    grid_x, grid_y, grid_z = get_grids(x, y, attr[1])
    print(grid_x)
    for pointx, pointy, labelz in (zip(x, y, attr[1])):
        if labelz > 0:
            ax.text(pointx, pointy, labelz, '%s' % (str(labelz)), size=7, zorder=1, c='blue')

    ax.plot_surface(grid_x, grid_y, grid_z, cmap=plt.cm.viridis)

    # Fixed label names for x and y
    ax.set_xlabel(label_names[0])
    ax.set_ylabel(label_names[1])
    ax.set_zlabel(label_names[2])

    ax.set_zlim(0, 1)
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.show()


def get_grids(x, y, label):
    """
    The function that returns a grid given x and y dimensions.

    :param list x: A list of values for a dimension.
    :param list y: A list of values for a dimension.
    :param label: A list of a dimension to the corresponding x, y point.
    :return: An array for grids x, y and z.

    """
    data = list(zip(x, y, label))
    x, y, label = zip(*data)
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]
    grid_z = griddata((x, y), label, (grid_x, grid_y), method='linear')
    grid_z[np.isnan(grid_z)] = 0
    return grid_x, grid_y, grid_z


def view_scatter_graph(df):
    """
    Function used for self-testing!
    The method the plots a 4 dimensional graph for joy and sadness from a dataframe.

    :param df: A dataframe (from gain_data.py) containing users, sentiment and track ids.

    """

    # Hardcoded printing first two variables after PCA
    # Function used for self-testing
    vx = 'pc1'
    vy = 'pc2'
    vz1 = 'joy'
    vz2 = 'sadness'

    fig1 = plt.figure()

    ax = fig1.add_subplot(projection='3d', zlim=(0, 1))

    # 4-dimensions
    ax.scatter(df[vx], df[vy], df[vz1], marker=".", edgecolors="black", linewidth=0.2, s=80, c='green')
    ax.scatter(df[vx], df[vy], df[vz2], marker=".", edgecolors="black", linewidth=0.2, s=80, c='blue')

    # 3-dimensions
    # img = ax.scatter(x, y, z, marker=".")

    ax.set_xlabel(vx)
    ax.set_ylabel(vy)
    ax.set_zlabel(vz1)
    plt.show()


def main():
    """
    The driver function of this file.

    """
    # w2, x2, y2, z2 = get_x_y_z(get_song_list_ids('78FHjijA1gBLuVx4qmcHq6'), vw, vx, vy, vz)
    # w3, x3, y3, z3 = get_x_y_z(get_song_list_ids('3aBeWOxyVcFupF8sKMm2k7'), vw, vx, vy, vz)
    # w3, x3, y3, z3 = get_x_y_z(recentlyPlayed.get_recently_played())

    # w1, x1, y1, z1 = get_x_y_z(get_song_list_ids('4ghvB1pIW4LTUn0RYrfuD5'), vw, vx, vy, vz)
    # graph_one_playlist(get_song_list_ids('0IAG5sPikOCo5nvyKJjCYo'))

    graph_one_playlist(get_song_list_ids('78FHjijA1gBLuVx4qmcHq6'))

    graph_one_playlist(get_song_list_ids('3tpc6g7KWkUF5TVt0zT8q6'))

    # w1, x1, y1, z1 = get_x_y_z(get_song_list_ids('3aBeWOxyVcFupF8sKMm2k7'), vw, vx, vy, vz)
    # graph_one_playlist(vx, vy, vz, w1, x1, y1, z1)
    # show_graph_sample(vx, vy, vz, x1, x2, x3, y1, y2, y3, z1, z2, z3)


# main()
# graph_one_playlist(get_recently_played(), label=False)
