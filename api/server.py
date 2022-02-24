# venv\Scripts\activate   - to run the venv from the api directory
# python server.py        - to run the server file

# python -m pip install --upgrade pip    - for pycharm

from twitter_data.secondPython import calc
from flask import Flask

app = Flask(__name__)


@app.route("/time")
def get_current_time():
    # return{'time': [time.time()]}
    return {'test var': []}


if __name__ == "__main__":
    app.run(debug=True)
