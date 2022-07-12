import uuid

from .models import Transaction, db

def addTransaction(uid, ticker, count, buy_price, sell_price, type):

	tid = str(uuid.uuid4())

	if type == 'buy':
		sell_price = None

	new_transaction = Transaction(tid=tid, uid=uid, buy_price=buy_price, sell_price=sell_price, type=type)

	db.session.add(new_transaction)
	db.session.commit()