import finnhub
import os
import json
import time

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def getPriceByTicker(ticker):

	starting_time = time.time()

	data = finnhub_client.quote(ticker)

	if data['c'] == 0:
		return False
	
	ending_time = time.time()
	print(ending_time-starting_time)
	return data['c']

def getPriceByTickerDev(ticker):

	FILE_PATH = '/Users/sidrachabathuni/Projects/eztrades/app/testAPI.json'

	with open(FILE_PATH, 'r') as s:
		file = json.load(s)
	
	try:
		price = file[ticker]
		return price
	except:
		return False
