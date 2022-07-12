from multiprocessing.dummy import current_process
from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, jsonify

import main.stock_api_actions

portfolio_info_page = Blueprint('portfolio_display_page', __name__, template_folder='../templates')

@portfolio_info_page.route('/portfolio/session')
def handleShowSession():
	if 'profile' not in session:
		return 'not logged in'
	
	return session


@portfolio_info_page.route('/stock/data')
def handleStockData():

	ticker = request.args['ticker']
	print(ticker)
	current_price = main.stock_api_actions.getPriceByTicker(ticker)


	return jsonify({'current_price': current_price})