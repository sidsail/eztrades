
# AS simeple as possbile flask google oAuth 2.0
from curses import noecho
from email.policy import default
from re import S
from statistics import mode
from textwrap import indent
from unicodedata import name


from flask import Flask, redirect, render_template, url_for, session, request, Blueprint
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from flask_cors import CORS
from pprint import pprint
import requests
from flask_sqlalchemy import SQLAlchemy




	
app = Flask(__name__)


CORS(app)
#config session
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/portfolios.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#databse shit


from database_layer import models

db = models.db
db.init_app(app)

with app.app_context():
	db.create_all()



#app = Flask(__name__)

#config session
#app.secret_key = os.getenv("APP_SECRET_KEY")
#app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
	name='google',
	client_id=os.getenv("GOOGLE_CLIENT_ID"),
	client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
	access_token_url='https://accounts.google.com/o/oauth2/token',
	access_token_params=None,
	authorize_url='https://accounts.google.com/o/oauth2/auth',
	authorize_params=None,
	api_base_url='https://www.googleapis.com/oauth2/v1/',
	userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
	client_kwargs={'scope': 'openid email profile'},
	jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)





@app.route('/')
def renderIndex():
	return render_template('index.html')




#routing imports

from blueprints.display import display_page
from blueprints.portfolio_data import portfolio_info_page
from blueprints.test import test_page
from blueprints.portfolio_actions import portfolio_actions

#routing split up

app.register_blueprint(display_page)
app.register_blueprint(portfolio_info_page)
app.register_blueprint(test_page)
app.register_blueprint(portfolio_actions)


from database_layer import users_db


#google oauth login stuff from here ^^^^ are the actual routes


@app.route('/login')
def login():
	google = oauth.create_client('google')  # create the google oauth client
	redirect_uri = url_for('authorize', _external=True)
	return google.authorize_redirect(redirect_uri)



@app.route('/authorize')
def authorize():
	google = oauth.create_client('google')  # create the google oauth client
	token = google.authorize_access_token()  # Access token from google (needed to get user info)
	resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
	user_info = resp.json()
	user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
	# Here you use the profile/user data that you got and query your database find/register the user
	# and set ur own data in the session not the profile from google
	session['profile'] = user_info
	session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
	#pprint(session)

	#add user to database
	user = users_db.addUser(session['profile']['email'])

	if user == False:
		pass
	
	session['uid'] = user.uid
	session['money'] = user.money

	return redirect('/display/portfolio')


@app.route('/logout')
def logout():
	for key in list(session.keys()):
		session.pop(key)
	return redirect('/')


