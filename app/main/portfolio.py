from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, abort, jsonify

from database import users_db, holdings_db
from . import stock_api_actions

def handleBuyStock(ticker, count: int):

	buy_price = stock_api_actions.getPriceByTicker(ticker)

	if buy_price == False:
		return jsonify({'success': False})
	
	uid = session['uid']
	money = session['money']

	money_needed = count * buy_price

	if money_needed > money:
		return jsonify({'success': 'money'})
	
	new_money = money - money_needed
	new_money = round(new_money, 2)

	session['money'] = new_money
	users_db.updateMoney(uid=uid, new_money=new_money)

	holdings_db.addHolding(uid=uid, ticker=ticker, count=count, buy_price=buy_price)
	return jsonify({'success': True})

def getHoldingsWithCurrentPrice(uid):

	holdings_obj = holdings_db.getTotalStockOwned(uid)

	for key in holdings_obj.keys():
		current_price = stock_api_actions.getPriceByTicker(key)
		holdings_obj[key]['current_price'] = current_price

	return holdings_obj