# venv\Scripts\activate   - to run the venv from the api directory
# python server.py        - to run the server file

# python -m pip install --upgrade pip    - for pycharm
from flask import Flask, request
from twitter_data.hashtag_search import _main_, predict_searched_song

app = Flask(__name__)

predict_id = ""


@app.route("/time")
def get_current_time():
    # return{'time': [time.time()]}
    return {'test var': []}


@app.route("/getPredictions")
def get_predictions():
    anger, fear, joy, sadness = _main_()
    anger = [element * 100 for element in anger]
    fear = [element * 100 for element in fear]
    joy = [element * 100 for element in joy]
    sadness = [element * 100 for element in sadness]

    return {'anger': [anger], 'fear': [fear], 'joy': [joy], 'sadness': [sadness]}


@app.route("/postPredictSong", methods=["POST", "GET"], strict_slashes=False)
def predict_this():
    global predict_id
    predict_id = request.json['trackid']
    return "Added"


@app.route("/getPredictSong", methods=["POST", "GET"], strict_slashes=False)
def get_pred():
    global predict_id
    print(predict_id)
    anger, fear, joy, sadness = predict_searched_song(predict_id)
    anger = [element * 100 for element in anger]
    fear = [element * 100 for element in fear]
    joy = [element * 100 for element in joy]
    sadness = [element * 100 for element in sadness]
    return {'anger': [anger], 'fear': [fear], 'joy': [joy], 'sadness': [sadness]}


if __name__ == "__main__":
    app.run(debug=True)
