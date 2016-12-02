from control import *
from json import load, dumps
from flask import Flask, request, send_from_directory
import requests

app = Flask(__name__)
jobs_url = "https://jobs.github.com/positions.json"

#----- SETUP ---------------------------------------------------------------------------------------

#This route allows javascript to include javascript files by saying src="/scripts/filepathgoeshere"
@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

#------ PAGES --------------------------------------------------------------------------------------

@app.route('/')
def root():
    return send_from_directory('views','index.html') #send_from_directory is safer

@app.route('/home')
def home_route():
    return send_from_directory('views','home.html')

@app.route('/edit_profile')
def edit_profile_route():
    #return send_from_directory('views','home.html')
    return ''

@app.route('/about')
def about_route():
    #return send_from_directory('views','home.html')
    return ''


#------ METHODS --------------------------------------------------------------------------------------
    
@app.route('/login', methods=['POST'])
def route_login_route():
    pass


@app.route('/get_jobs', methods=['POST'])
def get_jobs_route():
    return get_jobs(jobs_url,request.form['searchterm'])



app.run()