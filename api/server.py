# venv\Scripts\activate   - to run the venv from the api directory
# python server.py        - to run the server file

import time
from flask import Flask

app = Flask(__name__)

@app.route("/time")
def get_current_time():
    return{'time': [time.time()]}


if __name__ == "__main__":
    app.run(debug=True)
    