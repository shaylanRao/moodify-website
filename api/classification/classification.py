import math

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor

from spotipy_section.graphPlaylist import get_all_music_features


class LinLogReg:
    """
    This is a class that computes Linear and Logistic regression.

    Attributes:
        data: The user dataframe containing labels and attributes.
        emotion: The emotion defined for the model to train to label.

    """

    def __init__(self, data, emotion):
        """
        The constructor for LinLogReg class.

        :param data: The user dataframe containing labels and attributes.
        :param str emotion: The emotion defined for the model to train to label.

        """
        self.user_data = data
        self.EMOTION = emotion

    TRAIN_DATA_PROPORTION = 0.7
    LOG_THRESHOLD = 0.5
    DATA_PRESERVED = 0.95

    train_lbl = pd.Series
    test_lbl = pd.Series
    split_pos = 0
    train_data = pd.Series
    test_data = pd.Series

    scalar = None
    pca_model = None
    predict_playlist_data = None

    def prep_data(self):
        """
        The method to format the training data and test data for modeling.
        """

        # Gets the list of tracks from the user
        track_list = self.user_data['track_id'].tolist()

        # Gets the all the musical features of each song
        track_features = get_all_music_features(track_list)

        # Merges track features to the track and other data
        self.user_data = pd.concat([self.user_data, track_features], axis=1)
        # self.user_data.to_csv('userdata.csv')

        # Gets the size of the overall dataframe
        df_size = self.user_data.shape[1]

        # Randomizes rows
        shuffled_data = self.user_data.sample(frac=1)

        # Sets music components as data (and includes lyrical data if any is present)
        # (10 represents the number of music features)
        self.set_train_test_data(shuffled_data.iloc[:, df_size - 10:])

        # Sets music data to also include lyrical sentiment
        # self.set_train_test_data(shuffled_data.iloc[:, df_size-17:])

        # and anger to tentative as labels
        self.set_train_test_labels(shuffled_data.iloc[:, 2:9])

    def set_train_test_data(self, music_data):
        """
        The method that sets the train and test data for music attributes.

        :param music_data: Dataframe containing only music attributes and labels.

        """
        self.split_pos = math.ceil((len(music_data)) * self.TRAIN_DATA_PROPORTION)
        self.train_data = music_data.iloc[:self.split_pos, :]
        self.test_data = music_data.iloc[self.split_pos:, :]

    def set_train_test_labels(self, labels):
        """
        The method that sets the train and test data for music labels.

        :param labels: The labels to be set.

        """
        labels = labels[self.EMOTION]
        self.train_lbl = labels[:self.split_pos]
        self.test_lbl = labels[self.split_pos:]

    def get_log_data_labels(self, label):
        """
        The function to classify labels into either 1 or 0.

        :param label: The list of labels.
        :return: A list of labels of either 1 or 0.
        :rtype: list

        """
        log_label = [int(x >= self.LOG_THRESHOLD) for x in label.tolist()]
        return log_label

    # --- PCA (for use on ML techniques) ---
    def standardizer(self):
        """
        The method that standardises the both train and test data values by train set.

        """
        # define scalar
        scalar = StandardScaler()

        # fit scalar to training data only
        scalar.fit(self.train_data)
        self.scalar = scalar

        # Transform both datasets
        self.train_data = scalar.transform(self.train_data)
        self.test_data = scalar.transform(self.test_data)

    # PCA function
    def prin_comp(self):
        """
        The method that applies PCA to the train and test data.

        """
        # Keeps the relevant number of components to ensure 95% of original data is preserved
        pca = PCA(self.DATA_PRESERVED)
        pca.fit(self.train_data)

        self.pca_model = pca

        # Transform both data
        self.train_data = pca.transform(self.train_data)
        self.test_data = pca.transform(self.test_data)
        # print("Originality per dimension increase")
        # print(np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4) * 100))

    # --- Different models ---
    # Logistic regression modeling
    def log_reg_func(self):
        """
        The driver function that models the prepared data for logistic regression.

        :return: The logistic regression model.

        """
        log_reg_train_lbl = self.get_log_data_labels(self.train_lbl)
        logistic_reg = LogisticRegression(solver='lbfgs', fit_intercept=False)
        logistic_reg.fit(self.train_data, log_reg_train_lbl)
        return logistic_reg

    # Linear regression modeling
    def lin_reg_func(self):
        """
        The driver function  that models the prepared data for linear regression.

        :return: The linear regression model.

        """
        linear_reg = LinearRegression(positive=True, fit_intercept=False)
        linear_reg.fit(self.train_data, self.train_lbl)
        return linear_reg

    # Ridge
    def ridge_reg_func(self):
        """
        The driver function that models the prepared data for ridge regression.

        :return: The ridge regression model.

        """
        ridge_reg = Ridge(positive=True, fit_intercept=False)
        ridge_reg.fit(self.train_data, self.train_lbl)
        return ridge_reg

    # --- Testing different classification methods ---
    def log_reg_classifier(self):
        """
        The method that prints and compares logistic regression model prediction to actual data.

        """
        # applying logistic regression
        log_reg_model = self.log_reg_func()
        # predict all values
        print("Logistic Regression:")
        print("Actual:")
        print(self.get_log_data_labels(self.test_lbl))
        print("Predicted:")
        print(log_reg_model.predict(self.test_data))
        print("")

    def lin_reg_classifier(self):
        """
        The method that prints and compares linear regression model prediction to actual data.

        """
        lin_reg_model = self.lin_reg_func()
        # predicting all values
        print("Linear Regression:")
        print("Actual:")
        print(np.around(self.test_lbl.tolist(), 3))
        print("Predicted:")
        print(np.around(lin_reg_model.predict(self.test_data), 3))
        print("")

    def ridge_reg_classifier(self):
        """
        The method that prints and compares ridge regression model prediction to actual data.

        """
        ridge_reg_model = self.ridge_reg_func()
        # predict all values
        print("Ridge Regression:")
        print("Actual:")
        print(np.around(self.test_lbl.tolist(), 3))
        print("Predicted:")
        print(np.around(ridge_reg_model.predict(self.test_data), 3))
        print("")

    # --- Runs classification, choosing appropriate method
    def classify(self):
        """
        The driver method that prepares the data and executes model training functions.

        """
        # Gets formatted data for training and testing
        self.prep_data()
        # standardizes the data
        self.standardizer()
        # Does PCA on data
        self.prin_comp()

        self.log_reg_classifier()
        self.lin_reg_classifier()
        self.ridge_reg_classifier()

    # Evaluating metrics for models using predictions
    def evaluate_model(self, test_preds):
        """
        The method that prints evaluation metrics for models.

        """
        # Calculates mean squared error on test data
        mse = mean_squared_error(self.test_lbl, test_preds)
        rmse = math.sqrt(mse)

        # Generates pair-wise Pearsons correlation
        corr_matrix = self.user_data.corr()

        r2 = r2_score(self.test_lbl, test_preds)

        print("RSME:")
        print(rmse)
        print("")

        print("R2 Score:")
        print(r2)
        print("")

        # print("Correlation matrix:")
        # display(corr_matrix[self.EMOTION])
        print("----------------------------------")
        print("")


class KernelSVC(LinLogReg):
    """
    This is a class that computes Kernel Support Vector Classification (SVC), inherited from LinLogReg

    Attributes:
        data: The user dataframe containing labels and attributes.
        emotion: The emotion defined for the model to train to label.

    """
    def drive(self):
        """
        The driver method for preparing and training the model.

        """
        self.prep_data()
        self.standardizer()
        self.prin_comp()
        y_pred = self.kernel("gaus")
        self.eval(y_pred)

    def kernel(self, k_type):
        """
        The function that applies the chosen kernel function.

        :param str k_type: The type of kernel ('poly', 'gaus', 'sigmoid').
        :return: The predicted values for test data.

        """
        if k_type == "poly":
            sv_classifier = SVC(kernel='poly', degree=8)
        elif k_type == "gaus":
            sv_classifier = SVC(kernel='rbf')
        elif k_type == "sigmoid":
            sv_classifier = SVC(kernel='sigmoid')
        else:
            print("Used Default")
            sv_classifier = SVC(kernel='poly', degree=8)
        sv_classifier.fit(self.train_data, self.get_log_data_labels(self.train_lbl))
        y_pred = sv_classifier.predict(self.test_data)
        return y_pred
        # print("ACTUAL")
        # print(self.get_log_data_labels(self.test_lbl))
        # print("PREDICTION")
        # print(y_pred)

    def eval(self, y_pred):
        """
        The method that prints the confusion matrix and classification report on the model.

        :param y_pred: the predicted values for the test data.

        """
        print("Values")
        print(self.get_log_data_labels(self.test_lbl))
        print(y_pred)
        print(confusion_matrix(self.get_log_data_labels(self.test_lbl), y_pred))
        print(classification_report(self.get_log_data_labels(self.test_lbl), y_pred))



class KernelSVR(LinLogReg):
    def drive(self):
        pass


class KNeighborRegressor(LinLogReg):
    """
    A class that computes K-Nearest Neighbor Regressor, inherited from LinLogReg.

    Attributes:
        data: The user dataframe containing labels and attributes.
        emotion: The emotion defined for the model to train to label.

    """
    def drive(self):
        """
        The driver function that prepares the data and trains the model.

        :return: The model, the scalar transformation and pca fit (to be applied to new data).

        """
        print("KNR ", self.EMOTION, ":")
        self.prep_data()
        self.standardizer()
        self.prin_comp()
        max_n = math.floor(len(self.train_data) * (4 / 5))
        best_params = self.grid_search(KNeighborsRegressor(),
                                       {"n_neighbors": range(2, max_n), 'weights': ['uniform', 'distance'],
                                        "leaf_size": range(15, 30)})
        bagging_model = self.knr_bagging(best_params['n_neighbors'], best_params['leaf_size'], best_params['weights'])
        return bagging_model, self.scalar, self.pca_model
        # self.correlation_graph()

    def knr_bagging(self, k_num, leaf_sz, weight):
        """
        The function that takes the (optimal) parameters and returns a tuned model for KNR.

        :param int k_num: The number of clusters.
        :param int leaf_sz: Leaf size, maximum number of points from root node.
        :param str weight: How the points are weighted
        :return: The tuned model.

        """
        # Initialises KNR using optimal parameters
        tuned_knr = KNeighborsRegressor(n_neighbors=k_num, leaf_size=leaf_sz, weights=weight)
        print("k: ", k_num, " leaf: ", leaf_sz, " weights: ", weight)
        # Uses bagging to improve model
        bagging_model = BaggingRegressor(tuned_knr, n_estimators=1000)
        # Fits the bagged model to the training data with labels
        bagging_model.fit(self.train_data, self.train_lbl)
        # Makes predictions on test data using fitted model
        test_preds = bagging_model.predict(self.test_data)
        # Evaluates model using function
        self.evaluate_model(test_preds)
        # make prediction on playlist data
        return bagging_model
        # self.knr_boosting()

    # Boosting regressor instead of KNR and Bagging -- failed as overrides rpinciple of training a model
    # def knr_boosting(self):
    #     print("Boost model:")
    #     boost_model = GradientBoostingRegressor(random_state=0)
    #     boost_model.fit(self.train_data, self.train_lbl)
    #     test_preds = boost_model.predict(self.test_data)
    #     mse = mean_squared_error(self.test_lbl, test_preds)
    #     rmse = math.sqrt(mse)
    #     print(rmse)

    # Testing to see correlation for energy and loudness and prediction on colorbar
    def plot_model(self, test_preds):
        """
        The method that plots a heatmap graph of energy against loudness colour-coded by prediction.

        :param test_preds: ndarray of predictions.

        """
        cmap = sns.cubehelix_palette(as_cmap=True)
        f, ax = plt.subplots()
        points = ax.scatter(self.test_data['energy'], self.test_data['loudness'], c=test_preds, s=50, cmap=cmap)
        f.colorbar(points)
        plt.show()

    # Tuning
    def grid_search(self, model, params):
        """
        The function that executes a grid search to find optimal parameters for a model given train data.

        :param model: An empty instance of a chosen model.
        :param dict params: A dictionary of valid parameters and ranges of values for each for the model.
        :return: The optimal parameters.
        :rtype: dict

        """
        # Define range to test for parameters
        parameters = params
        gridsearch = GridSearchCV(model, parameters)
        # Find the parameters for the given data
        gridsearch.fit(self.train_data, self.train_lbl)
        # Returns the optimal parameters for the training data
        return gridsearch.best_params_


class DecisionTree(KNeighborRegressor):
    """
    A class that computes a decision tree regressor model, inherited from KNeighborRegressor.

    Attributes:
        data: The user dataframe containing labels and attributes.
        emotion: The emotion defined for the model to train to label.

    """
    def drive(self):
        """
        The driver function that prepares the data and trains the model.

        :return: The model, the scalar transformation and pca fit (to be applied to new data).

        """
        print("Dec Tree Reg ", self.EMOTION, ":")
        self.prep_data()
        self.standardizer()
        self.prin_comp()
        dec_tree = self.decision_tree_regressor()
        return dec_tree, self.scalar, self.pca_model
        # self.correlation_graph()

    def decision_tree_regressor(self):
        """
        The function that computes the optimal parameters and trains a decision tree.

        :return: The decision tree model.
        """
        parameters = {"splitter": ["best", "random"],
                      "max_depth": [3, 5, 7, 9],
                      "min_samples_leaf": [1, 2, 3, 4, 5],
                      "min_weight_fraction_leaf": [0.1, 0.2, 0.3, 0.4],
                      "max_features": ["auto", "log2", "sqrt", None],
                      "max_leaf_nodes": [None, 10, 20, 30, 40, 50]}

        # dec_tree = DecisionTreeRegressor()
        # dec_tree = dec_tree.fit(self.train_data, self.train_lbl)
        # test_preds = dec_tree.predict(self.test_data)
        # print("dec tree score")
        # print(dec_tree.score(self.test_data, self.test_lbl))

        # if self.EMOTION == "joy":
        # sns.distplot(test_preds)
        best_params = self.grid_search(DecisionTreeRegressor(), parameters)
        # print(best_params)
        tuned_dec_tree = DecisionTreeRegressor(max_depth=best_params['max_depth'],
                                               max_features=best_params['max_features'],
                                               max_leaf_nodes=best_params['max_leaf_nodes'],
                                               min_samples_leaf=best_params['min_samples_leaf'],
                                               min_weight_fraction_leaf=best_params['min_weight_fraction_leaf'],
                                               splitter=best_params['splitter'])

        bag_tuned_dec_tree = BaggingRegressor(tuned_dec_tree, n_estimators=1000, max_features=5, max_samples=8)
        bag_tuned_dec_tree.fit(self.train_data, self.train_lbl)
        print("bagged dec tree score")
        print(bag_tuned_dec_tree.score(self.test_data, self.test_lbl))
        test_preds = bag_tuned_dec_tree.predict(self.test_data)

        self.evaluate_model(test_preds)

        return bag_tuned_dec_tree
