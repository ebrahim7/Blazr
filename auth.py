#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session
import json

   
def oauth_decode(data):
  import json
  new_data = data.decode("utf-8", "strict")

  return json.loads(new_data)
  
class OAuthSignIn(object):
  providers = None

  def __init__(self, provider_name):
    self.provider_name = provider_name
    credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
    self.consumer_id = credentials['id']
    self.consumer_secret = credentials['secret']

  def authorize(self):
    pass

  def callback(self):
    pass

  def get_callback_url(self):
    return url_for('oauth_callback', provider=self.provider_name,
                   _external=True)

  @classmethod
  def get_provider(self, provider_name):
    if self.providers is None:
      self.providers = {}
      for provider_class in self.__subclasses__():
        provider = provider_class()
        self.providers[provider.provider_name] = provider
    return self.providers[provider_name]

class LinkedInSignIn(OAuthSignIn):
  def __init__(self):
    super(LinkedInSignIn, self).__init__('linkedin')
    self.service = OAuth2Service(
      name='linkedin',
      client_id=self.consumer_id,
      client_secret=self.consumer_secret,
      authorize_url='https://www.linkedin.com/uas/oauth2/authorization',           
      access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
      base_url='https://www.linkedin.com/'
    )
      
  def authorize(self):
    return redirect(self.service.get_authorize_url(
      #scope='email', #set by default in the linkedIn application configuration
      response_type='code',
      state=current_app.config['OAUTH_CREDENTIALS']['linkedin']['state'],
      redirect_uri=self.get_callback_url())
    )
    
  
  def callback(self):
    if 'code' not in request.args:
      return None, None, None
    if 'state' in request.args:
      print ('state: ', request.args.get('state'))
      
    credentials = current_app.config['OAUTH_CREDENTIALS']['linkedin']
    if request.args.get('state') != credentials['state']:
      print('THIS SHOULD THROW 401 ERROR BECAUSE STATE IS NOT THE SAME')
    #json_decoder = json.loads
    #params = {'decoder': oauth_decode}
    
    data = {'code': request.args['code'],
          'grant_type': 'authorization_code',
          'redirect_uri': self.get_callback_url()}
    #response = self.service.get_raw_access_token(data=data)
    #response = response.json()
    
    oauth_session = self.service.get_auth_session( 
      data=data,
      decoder = oauth_decode
    )
    print('response: ',oauth_session.get('v1/people/~?format=json')) 
#    print((oauth_session.get('me')).read().decode('utf-8'))
    #me = oauth_session.get('v1/people/~?format=json').json()
    me = oauth_session.get('v1/people/~:(id,firstName,lastName,headline,picture-url,email_address)?format=json').json()
    print(me)
    return (
      'linkedin$' + me['id'],
      me.get('firstName') + ' ' + me.get('lastName'),
      me.get('headline'),
      me.get('emailAddress')
    )