from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, abort, jsonify

portfolio_actions = Blueprint('portfolio_actions', __name__, template_folder='../templates')

from database import holdings_db
from main import stock_api_actions
from main import portfolio

@portfolio_actions.route('/addstock', methods = ['POST'])
def handleAddStock():

	if 'profile' not in session:
		return 'not logged in'
	
	args = request.args

	try:
		count = int(args['count'])
		ticker = args['ticker']
	except:
		abort(403) 
	

	return portfolio.handleBuyStock(ticker, count)

	