from hashlib import new
from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, abort, jsonify
import math

from database_layer import users_db, holdings_db, transactions_db
from . import stock_api_actions

def handleBuyStock(ticker, count: int):

	buy_price = stock_api_actions.getPriceByTicker(ticker)
	#buy_price = stock_api_actions.getPriceByTickerDev(ticker)
	if buy_price == False:
		return jsonify({'success': False, 'error': 'ticker does not exist'})
	
	uid = session['uid']
	money = session['money']

	money_needed = count * buy_price

	if money_needed > money:
		return jsonify({'success': False, 'error': 'not enough money'})
	
	new_money = money - money_needed
	new_money = round(new_money, 2)

	session['money'] = new_money
	users_db.updateMoney(uid=uid, new_money=new_money)

	holdings_db.addHolding(uid=uid, ticker=ticker, count=count, buy_price=buy_price)
	return jsonify({'success': True, 'new_money': new_money, 'value': abs(money-new_money)})



def handleSellStock(ticker, count: int):

	uid = session['uid']
	current_stock_price = stock_api_actions.getPriceByTicker(ticker)
	#current_stock_price = stock_api_actions.getPriceByTickerDev(ticker)
	
	if holdings_db.deleteHolding(uid, ticker, count, sell_price=current_stock_price) == False:
		return jsonify({'success': False, 'error': 'trying to sell more than have'})
	
	
	money = session['money']
	money_recieved_from_sale = count * current_stock_price

	new_money = round(money + money_recieved_from_sale, 2)
	
	users_db.updateMoney(uid, new_money)
	session['money'] = new_money


	return jsonify({'success': True, 'new_money': new_money, 'value': abs(money-new_money)})



def getHoldingsWithCurrentPrice(uid):

	holdings_obj = holdings_db.getTotalStockOwned(uid)

	for key in holdings_obj.keys():
		current_price = stock_api_actions.getPriceByTicker(key)
		#current_price = stock_api_actions.getPriceByTickerDev(key)
		holdings_obj[key]['current_price'] = current_price

	money = session['money']
	holdings_obj['money'] = money

	print(holdings_obj)

	return holdings_obj

def getTransactionHistory(uid):


	transactions_arr = transactions_db.getTransactionHistory(uid)

	print(transactions_arr)

	return jsonify({'transactions': transactions_arr})
