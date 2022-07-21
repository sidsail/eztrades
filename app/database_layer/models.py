from email.policy import default
from xmlrpc.client import FastMarshaller
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import date, datetime

db = SQLAlchemy()

class User(db.Model):

	__tablename__ = 'users'

	uid = db.Column(db.String, primary_key=True)
	email = db.Column(db.String, unique=True, nullable=False)
	money = db.Column(db.Float, default=100000, nullable=False)
	created = db.Column(db.DateTime(timezone=True), server_default=func.now())


class Holding(db.Model):

	__tablename__ = 'holdings'

	hid = db.Column(db.String, primary_key=True)
	uid = db.Column(db.String, nullable=False)
	ticker = db.Column(db.String, nullable=False)
	count = db.Column(db.Integer, nullable=False)
	buy_price = db.Column(db.Float, nullable=False)
	created = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Transaction(db.Model):

	__tablename__ = 'transactions'

	tid = db.Column(db.String, primary_key=True)
	uid = db.Column(db.String, nullable=False)
	ticker = db.Column(db.String, nullable=False)
	count = db.Column(db.Integer, nullable=False)
	buy_price = db.Column(db.Float, nullable=False)
	sell_price = db.Column(db.Float)
	action = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Queue(db.Model):

	__tablename__ = 'queue'

	qid = db.Column(db.String, primary_key=True)
	uid = db.Column(db.String, nullable=False)
	ticker = db.Column(db.String, nullable=False)
	count = db.Column(db.Integer, nullable=False)
	buy_price = db.Column(db.Float)
	sell_price = db.Column(db.Float)
	action = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime(timezone=True), server_default=func.now())
	