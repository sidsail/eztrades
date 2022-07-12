from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, jsonify


test_page = Blueprint('test_page', __name__, template_folder='../templates')

from database import users_db, holdings_db

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
