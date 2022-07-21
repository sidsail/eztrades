from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, abort, jsonify
import time

from database_layer import queue_db, users_db
import stock_api_actions

def resolveQueue():
	print('...')
	time.sleep(1)

def buyQueue(ticker, count: int):

	money = session['money']
	money_needed = count * money


	if money_needed > money:
		return jsonify({'success': False, 'error': 'not enough money'})

	uid = session['uid']
	buy_price = stock_api_actions.getPriceByTicker(ticker)
	if buy_price == False:
		return jsonify({'success': False, 'error': 'ticker does not exist'})



	queue_db.addBuyQueue(uid, ticker, count, buy_price)

	new_money = money - money_needed

	users_db.updateMoney(new_money)
	session['money'] = new_money

	return jsonify({'success': True})



