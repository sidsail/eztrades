from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import date, datetime

db = SQLAlchemy()

class User(db.Model):

	__tablename__ = 'users'

	uid = db.Column(db.String, primary_key=True)
	email = db.Column(db.String, unique=True, nullable=False)
	money = db.Column(db.Float, default=100000, nullable=False)
	created = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class Holding(db.Model):

	__tablename__ = 'holdings'

	hid = db.Column(db.String, primary_key=True)
	uid = db.Column(db.String, nullable=False)
	ticker = db.Column(db.String, nullable=False)
	count = db.Column(db.Integer, nullable=False)
	buy_price = db.Column(db.Float, nullable=False)
	created = db.Column(db.DateTime, default=datetime.now(), nullable=False)

class Transaction(db.Model):

	__tablename__ = 'transactions'

	tid = db.Column(db.String, primary_key=True)
	uid = db.Column(db.String, nullable=False)
	ticker = db.Column(db.String, nullable=False)
	count = db.Column(db.Integer, nullable=False)
	buy_price = db.Column(db.Float, nullable=False)
	sell_price = db.Column(db.Float)
	type = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
