import finnhub
import os

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def getPriceByTicker(ticker):

	data = finnhub_client.quote(ticker)

	if data['c'] == 0:
		return False
	
	return data['c']