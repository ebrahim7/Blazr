#custom imported files
from control import *
from auth import *
#imported libraries
from json import load, dumps
from flask import Flask, request, send_from_directory, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import requests
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

app = Flask(__name__) #done in config.py
with app.app_context():
  # within this block, current_app points to app.
  app.config.from_object('config')
  print (current_app.name)
jobs_url = "https://jobs.github.com/positions.json"
provider_name = 'linkedin'
credentials = app.config['OAUTH_CREDENTIALS'][provider_name]
print('credentials: ',credentials)
#----- SETUP ---------------------------------------------------------------------------------------

#This route allows javascript to include javascript files by saying src="/scripts/filepathgoeshere"
@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

db = SQLAlchemy(app)
lm = LoginManager(app)

engine = create_engine("sqlite:///db.sqlite")  # Access the DB Engine
if not engine.dialect.has_table(engine, 'users'):  # If table don't exist, Create.
  metadata = MetaData(engine)
  # Create a table with the appropriate Columns
  Table('users', metadata,
        Column('id', Integer, primary_key=True, nullable=False), 
        Column('social_id', String, nullable=False), 
        Column('nickname', String, nullable=False),
        Column('headline', String),
        Column('emailaddress', String, nullable=False))
  # Implement the creation
  metadata.create_all()

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  social_id = db.Column(db.String(64), nullable=False, unique=True)
  nickname = db.Column(db.String(64), nullable=False)
  headline = db.Column(db.String(64), nullable=True)
  emailaddress = db.Column(db.String(64), nullable=False)

@lm.user_loader #This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object
def load_user(id):
  return User.query.get(int(id))
    
#------ PAGES --------------------------------------------------------------------------------------

@app.route('/')
def index():
  return render_template('index.html') 

@app.route('/profile')
@login_required
def profile():
  return render_template('profile.html')
    
@app.route('/home')
def home_route():
  return send_from_directory('views','home.html') #send_from_directory is safer

@app_route("/myprofile")
def myporfile_route():
	return send_from_directory('views','myprofile.html')

@app.route('/about')
def about_route():
  #return send_from_directory('views','home.html')
  return ''


#------ METHODS --------------------------------------------------------------------------------------
    
@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
  if not current_user.is_anonymous:
    return redirect(url_for('index'))
  oauth = OAuthSignIn.get_provider(provider)
  return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
  if not current_user.is_anonymous:
    return redirect(url_for('index'))
  oauth = OAuthSignIn.get_provider(provider)
  social_id, username, headline, emailaddress = oauth.callback()
  
  if social_id is None:
    flash('Authentication failed.')
    return redirect(url_for('index'))
  user = User.query.filter_by(social_id=social_id).first()
  if not user:
    user = User(social_id=social_id, nickname=username, headline=headline, emailaddress=emailaddress)
    db.session.add(user)
    db.session.commit()
    
  login_user(user, True)
  print('Logged in successfully.')

  next = request.args.get('next')
  # is_safe_url should check if the url is safe for redirects.
  # See http://flask.pocoo.org/snippets/62/ for an example.
  #if not is_safe_url(next):
  #    return abort(400)
  
  return redirect(url_for('profile'))
    
@app.route('/get_jobs', methods=['POST'])
def get_jobs_route():
  return get_jobs(jobs_url,request.form['searchterm'])



app.run()
