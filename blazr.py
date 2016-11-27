from json import load, dumps
from flask import Flask, request, render_template, url_for, redirect, jsonify
import requests

app = Flask(__name__)
jobs_url = "https://jobs.github.com/positions.json"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/jobs', methods=['POST'])
def jobs():
    searchterm=request.form['searchterm']
    print('searchterm: {}'.format(searchterm))
    response = requests.get(jobs_url, params={'description': searchterm})
    return response.text

app.run()