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
        Column('picture-url', String),
        Column('nickname', String, nullable=False),
        Column('headline', String),
        Column('summary', String),
        Column('experience', String),
        Column('skills', String),
        Column('phone', String),
        Column('emailaddress', String, nullable=False))
  # Implement the creation
  metadata.create_all()

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  social_id = db.Column(db.String(64), nullable=False, unique=True)
  picture-url = db.Column(db.String(64), nullable=True)
  nickname = db.Column(db.String(64), nullable=False)
  headline = db.Column(db.String(64), nullable=True)
  summary = db.Column(db.String(64), nullable=True)
  experience = db.Column(db.String(64), nullable=True)
  skills = db.Column(db.String(64), nullable=True)
  phone = db.Column(db.String(64), nullable=True)
  emailaddress = db.Column(db.String(64), nullable=False)

@lm.user_loader #This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object
def load_user(id):
  return User.query.get(int(id))
  
jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
  block_start_string='<%',
  block_end_string='%>',
  variable_start_string='%%',
  variable_end_string='%%',
  comment_start_string='<#',
  comment_end_string='#>'
))
app.jinja_options = jinja_options
    
#------ PAGES --------------------------------------------------------------------------------------

@app.route('/')
def index():
  return render_template('index.html') 

@app.route('/home')
def home_route():
  return send_from_directory('views','home.html') #send_from_directory is safer

@app.route("/myprofile")
@login_required
def myprofile_route():
	return render_template('myprofile.html')

@app.route('/about')
def about_route():
  #return send_from_directory('views','home.html')
  return ''
  
@app.route('/login_page')
def login_page_route():
  return render_template('login.html')


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
  social_id, username, headline, picture-url, emailaddress = oauth.callback()
  
  if social_id is None:
    flash('Authentication failed.')
    return redirect(url_for('index'))
  user = User.query.filter_by(social_id=social_id).first()
  if not user:
    user = User(social_id=social_id, nickname=username, headline=headline, picture-url=picture-url, emailaddress=emailaddress)
    db.session.add(user)
    db.session.commit()
  
  login_user(user, True)
  print('Logged in successfully.')

  next = request.args.get('next')
  # is_safe_url should check if the url is safe for redirects.
  # See http://flask.pocoo.org/snippets/62/ for an example.
  #if not is_safe_url(next):
  #    return abort(400)
  
  return redirect(url_for('myprofile_route'))
    
@app.route('/get_jobs', methods=['POST'])
def get_jobs_route():
  return get_jobs(jobs_url,request.form['searchterm'])

@app.route('/edit_user_info', methods=['POST'])
@login_required
def edit_user_info():
  entry_name = request.form['entry_name']
  entry = request.form['entry']
  print('Editing entry: {} with {}'.format(entry_name, entry))
  print('Editing user: {}'.format(current_user))
  #print('Changing user\'s {} from \"{}\" to \"{}\"'.format(entry, current_user[entry], request.form[entry]))
  
  app_edit_entry(entry_name, entry)
  print(url_for('myprofile_route'))
  return json.dumps({'status':'OK','url':url_for('myprofile_route')});
  
def app_edit_entry(entry_name, entry):
  if entry_name == 'nickname':
    current_user.nickname = entry
    db.session.commit()
  elif entry_name == 'summary':
    current_user.summary = entry
    db.session.commit()
  elif entry_name == 'experience':
    current_user.experience = entry
    db.session.commit()
  elif entry_name == 'skills':
    current_user.skills = entry
    db.session.commit()
  elif entry_name == 'emailaddress':
    current_user.emailaddress = entry
    db.session.commit()
  elif entry_name == 'phone':
    current_user.phone = entry
    db.session.commit()
  
app.run()
