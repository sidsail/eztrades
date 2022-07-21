from contextlib import nullcontext
from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, abort, jsonify

from .models import Queue, db

def addBuyQueue(uid, ticker, count: int, buy_price: float):

	new_queue_element = Queue(uid=uid, ticker=ticker, count=count, buy_price=buy_price, sell_price=None, action='buy')

	db.session.add(new_queue_element)
	db.session.commit()

def addSellQueue(uid, ticker, count: int, buy_price: float, sell_price: float)

	new_queue_element = Queue(uid=uid, ticker=ticker, count=count, buy_price=buy_price, sell_price=sell_price)

	db.session.add(new_queue_element)
	db.session.commit()
