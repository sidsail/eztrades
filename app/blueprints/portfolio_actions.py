from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, abort, jsonify

portfolio_actions = Blueprint('portfolio_actions', __name__, template_folder='../templates')

from database_layer import holdings_db, users_db, transactions_db
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


@portfolio_actions.route('/sellstock', methods=['DELETE'])
def handleSellStock():

	if 'profile' not in session:
		return 'not logged in'

	args = request.args

	count = int(args['count'])
	ticker = args['ticker']
	uid = session['uid']
	
	if holdings_db.deleteHolding(uid, ticker, count) == False:
		return jsonify({'success': False})
	
	current_stock_price = stock_api_actions.getPriceByTicker(ticker)
	money = session['money']
	money_recieved_from_sale = count * current_stock_price

	new_money = round(money + money_recieved_from_sale, 2)
	
	users_db.updateMoney(uid, new_money)
	session['money'] = new_money


	return jsonify({'success': True})

@portfolio_actions.route('/holdings')
def handleGetHoldings():
	if 'profile' not in session:
		return 'not logged in'

	uid = session['uid']
	return portfolio.getHoldingsWithCurrentPrice(uid)

	