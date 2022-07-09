# AS simeple as possbile flask google oAuth 2.0
from curses import noecho
from textwrap import indent

from flask import Flask, redirect, render_template, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from flask_cors import CORS
from pprint import pprint
import requests
import sqlite3



#from dotenv import load_dotenv
#load_dotenv()





#app = Flask(__name__)
#CORS(app)

#PORT = 3000


# Session config


def routes(app):


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
	def hello_world():
		return render_template('index.html')


	@app.route('/display/portfolio')
	def handleHome():
		if 'profile' not in session:
			return redirect('/')
		
		email = dict(session)['profile']['email']
		
		#add user to database if does not exist
		return render_template('portfolio.html')
	


	@app.route('/portfolio/session')
	def handleGetSession():
		if 'profile' not in session:
			return redirect('/')

		return session



	@app.route('/test')
	def test():
		if 'profile' not in session:
			return 'not logged in'

		return 'logged in'



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
		pprint(session)
		return redirect('/display/portfolio')


	@app.route('/logout')
	def logout():
		for key in list(session.keys()):
			session.pop(key)
		return redirect('/')

def create_app(test_config=None):
	app = Flask(__name__)

	#config session
	app.secret_key = os.getenv("APP_SECRET_KEY")
	app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
	app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

	#config database
	app.config['DATABASE'] = os.path.join(app.instance_path, 'portoflios.sqlite')
	#print(app.instance_path)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	routes(app)

	import db
	
	db.init_app(app)

	return app






