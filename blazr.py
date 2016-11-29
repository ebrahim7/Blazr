from json import load, dumps
from flask import Flask, request, render_template, url_for, redirect, jsonify, send_from_directory
import requests

app = Flask(__name__, static_url_path='/')
jobs_url = "https://jobs.github.com/positions.json"

#This route allows javascript to include javascript files by saying src="/scripts/filepathgoeshere"
@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

@app.route('/')
def root():
	return send_from_directory('views','index.html') #send_from_directory is safer

@app.route('/home')
def home():
	return send_from_directory('views','home.html')
	
@app.route('/jobs', methods=['POST'])
def jobs():
    searchterm=request.form['searchterm']
    print('searchterm: {}'.format(searchterm))
    response = requests.get(jobs_url, params={'description': searchterm})
    return response.text

app.run()