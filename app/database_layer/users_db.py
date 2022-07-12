from re import U
import uuid
import math

from .models import db, User

def addUser(email):

	new_user = User(uid=str(uuid.uuid4()), email=email, money=100000)

	user = User.query.filter_by(email=email).first()

	if bool(user) == True:
		return user


	db.session.add(new_user)
	db.session.commit()

	print('added ', email)
	return new_user

def getUserByEmail(email):

	user = User.query.filter_by(email=email).first()

	return user


def updateMoney(uid, new_money: float):

	user = User.query.filter_by(uid=uid).first()

	if bool(user) == False:
		return False
	
	user.money = round(new_money, 2)

	db.session.add(user)
	db.session.commit()

	return user