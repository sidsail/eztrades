from flask import Flask, redirect, render_template, url_for, session, request, Blueprint


display_page = Blueprint('display_page', __name__, template_folder='../templates')

@display_page.route('/blueprint/test')
def show():

	if 'profile' not in session:
		return 'not logged in'
	
	return render_template('test.html')


@display_page.route('/display/portfolio')
def handleDisplayPortfolio():
	if 'profile' not in session:
		return 'not logged in'
	
	return render_template('portfolio.html')