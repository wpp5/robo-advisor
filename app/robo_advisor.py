# this is the "app/robo_advisor.py" file

import os
import csv
import json
import requests

from dotenv import load_dotenv

#
# INFO INPUTS
#

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response = requests.get(request_url)

#print(type(response))
#print(response.status_code)
#print(response.status_code)
#print(response.text)



seg_response = json.loads(response.text)
last_refreshed = seg_response["Meta Data"]["3. Last Refreshed"]
latest_close = seg_response["Time Series (Daily)"]["2021-03-04"]["4. close"]

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
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-----")