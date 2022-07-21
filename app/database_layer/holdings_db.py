import uuid
from flask import jsonify

from .models import db, Holding
from . import transactions_db

def addHolding(uid, ticker, count: int, buy_price: int):


	new_holding = Holding(hid=str(uuid.uuid4()), uid=uid, ticker=ticker, count=count, buy_price=buy_price)

	holding = Holding.query.filter_by(uid=uid, buy_price=buy_price).first()

	if bool(holding) == True:
		print(holding.count)
		holding.count += count
		db.session.add(holding)
		db.session.commit()
		transactions_db.addBuyTransaction(uid, ticker, count, buy_price)
		return new_holding

	db.session.add(new_holding)
	db.session.commit()

	transactions_db.addBuyTransaction(uid, ticker, count, buy_price)

	return new_holding


def getTotalStockOwned(uid):

	holdings = Holding.query.filter_by(uid=uid).all()
	print(holdings)

	holdings_object = {}

	for holding in holdings:
		if holding.ticker in holdings_object:
			holdings_object[holding.ticker]['count'] += holding.count
		
		else:
			holdings_object[holding.ticker] = {}
			holdings_object[holding.ticker]['count'] = holding.count



	return holdings_object

def deleteHolding(uid, ticker, count: int, sell_price):

	print(uid)
	holdings = Holding.query.filter_by(uid=uid, ticker=ticker)

	total_owned = 0
	for holding in holdings:
		total_owned += holding.count

	print(total_owned)

	if total_owned < count:
		return False

	for holding in holdings:

		if count >= holding.count:
			#count -= holding.count
			buy_price = holding.buy_price
			db.session.delete(holding)
			transactions_db.addSellTransaction(uid, ticker, count, buy_price, sell_price)

		else:
			holding.count -= count
			buy_price = holding.buy_price
			db.session.add(holding)
			transactions_db.addSellTransaction(uid, ticker, count, buy_price, sell_price)
	
	db.session.commit()



	return True


