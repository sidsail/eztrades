import uuid
from sqlalchemy import desc

from .models import Transaction, db

def addBuyTransaction(uid, ticker, count: int, buy_price: float):

	tid = str(uuid.uuid4())

	new_transaction = Transaction(tid=tid, uid=uid, ticker=ticker, count=count, buy_price=buy_price, sell_price=None, action='buy')

	db.session.add(new_transaction)
	db.session.commit()
	print(new_transaction.ticker, new_transaction.count, new_transaction.action)

	return True

def addSellTransaction(uid, ticker, count: int, buy_price: float, sell_price: float):
	
	tid = str(uuid.uuid4())

	new_transaction = Transaction(tid=tid, uid=uid, ticker=ticker, count=count, buy_price=buy_price, sell_price=sell_price, action='sell')

	db.session.add(new_transaction)
	db.session.commit()

	print


def getTransactionHistory(uid):

	transactions = Transaction.query.filter_by(uid=uid).order_by(desc(Transaction.created))

	transactions_arr = []

	for transaction in transactions:
		transaction_obj = {}
		transaction_obj['ticker'] = transaction.ticker
		transaction_obj['count'] = transaction.count
		transaction_obj['buy_price'] = transaction.buy_price
		transaction_obj['sell_price'] = transaction.sell_price
		transaction_obj['action'] = transaction.action
		transaction_obj['created'] = transaction.created
		transactions_arr.append(transaction_obj)
	
	return transactions_arr