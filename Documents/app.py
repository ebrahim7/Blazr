from json import load, dumps
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    pos = requests.get("http://jobs.github.com/positions.json").text
    return pos

app.run()