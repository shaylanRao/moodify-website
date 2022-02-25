# venv\Scripts\activate   - to run the venv from the api directory
# python server.py        - to run the server file

# python -m pip install --upgrade pip    - for pycharm

from flask import Flask
from twitter_data.hashtagSearch import _main_
import numpy as np

app = Flask(__name__)


@app.route("/time")
def get_current_time():
    # return{'time': [time.time()]}
    return {'test var': []}


@app.route("/getPredictions")
def get_predictions():
    anger, fear, joy, sadness = _main_()
    return {'anger': [anger], 'fear': [fear], 'joy': [joy], 'sadness': [sadness]}


if __name__ == "__main__":
    app.run(debug=True)
