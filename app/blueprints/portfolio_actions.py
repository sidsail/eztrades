from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, abort, jsonify

portfolio_actions = Blueprint('portfolio_actions', __name__, template_folder='../templates')

from database_layer import holdings_db, users_db, transactions_db
from main import stock_api_actions
from main import portfolio



@portfolio_actions.route('/portfolio/holdings')
def handleGetHoldings():
	if 'profile' not in session:
		return 'not logged in'

	uid = session['uid']
	return portfolio.getHoldingsWithCurrentPrice(uid)

@portfolio_actions.route('/portfolio/transactions')
def handleGetTransactions():

	if 'profile' not in session:
		return 'not logged in'
	
	uid = session['uid']

	return portfolio.getTransactionHistory(uid)



@portfolio_actions.route('/portfolio/action', methods = ['POST'])
def handleStockAction():

	if 'profile' not in session:
		return 'not logged in'

	args = request.args
	try:
		count = int(args['count'])

	except:
		abort(403)
	
	ticker = args['ticker']
	action = args['action']
	
	if action == 'buy':

		return portfolio.handleBuyStock(ticker, count)
	
	if action == 'sell':

		return portfolio.handleSellStock(ticker, count)
	
	