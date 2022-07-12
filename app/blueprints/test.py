from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, jsonify


test_page = Blueprint('test_page', __name__, template_folder='../templates')

from database import users_db, holdings_db
from main import stock_api_actions

@test_page.route('/database/users/test')
def handleUserTest():
	email = request.args['email']

	new_user = users_db.addUser(email)

	return new_user.email


@test_page.route('/database/holdings/test')
def handleHoldingTest():
	uid = request.args['uid']
	ticker = request.args['ticker']
	count = int(request.args['count'])
	buy_price = int(request.args['buy_price'])

	new_holding = holdings_db.addHolding(uid, ticker, count, buy_price)
	return "done, {}".format(ticker)

@test_page.route('/database/getholdings')
def handleTestGetHoldings():

	if 'profile' not in session:
		return 'not logged in'

	uid = session['uid']

	return holdings_db.getTotalStockOwned(uid)

