# this is the "app/robo_advisor.py" file

import os
import csv
import json
import requests


from dotenv import load_dotenv

load_dotenv()

#
# INFO INPUTS
#

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response = requests.get(request_url)

#print(type(response))
#print(response.status_code)
#print(response.status_code)
#print(response.text)


latest_day = "2021-03-04"

seg_response = json.loads(response.text)

last_refreshed = seg_response["Meta Data"]["3. Last Refreshed"]

tsd = seg_response["Time Series (Daily)"]

dates = list(tsd.keys()) # TODO: Sort so latest day is first

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

high_prices = []
#maximum of all high prices
for date in dates:
    high_price = tsd[latest_day]["2. high"]
    high_prices.append(float(high_price))
    

recent_high = max(high_prices)



def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-----")