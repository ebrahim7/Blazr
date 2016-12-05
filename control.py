from json import load, dumps
import requests
from flask_login import current_user
def login(data):
	uname = data['uname']
	password = data['password']
	key = data['key']
	return 'logged in'

def create_account(data):
	uname = data['uname']
	password = data['password']
	key = data['key']
	return 'created'

def get_jobs(jobs_url,term):
    response = requests.get(jobs_url, params={'description': term})
    return response.text
    
def like_job(data):
	# store job data in user DB
	return 'liked'
    
def app_edit_bio(data):
	uname = data['uname']
	bio = data['bio']
	return 'success'

def app_add_skill(data):
	uname = data['uname']
	skill = data['skill']
	return 'success'

def app_remove_skill(data):
	uname = data['uname']
	skill = data['skill']
	return 'success'


def app_remove_skill(data):
	uname = data['uname']
	skill = data['skill']
	return 'success'
	
def app_add_experience(data):
	uname = data['uname']
	exp = data['experience']
	return 'success'

def app_remove_experience(data):
	uname = data['uname']
	exp = data['experience']
	return 'success'

