from flask import Flask, request

from data.data_helper import DataHelper

app = Flask(__name__)

@app.route('/api/winner', methods=['GET'])
def index():
    params = request.args
    election_data = DataHelper(params)
    print(params)
    print(election_data.election_data)
    return "hi"
