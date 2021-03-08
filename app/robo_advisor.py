# this is the "app/robo_advisor.py" file

import os
import csv
import json
import requests
import datetime
import time

from dotenv import load_dotenv

load_dotenv()

#
# INFO INPUTS
#

apikey = os.environ.get("ALPHAVANTAGE_API_KEY")
while True:
    try: 
        symbol = input("Enter stock symbol for analysis. For example, AAPL, JNJ, etc.").upper()
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}"
        response = requests.get(request_url)

        seg_response = json.loads(response.text)

        last_refreshed = seg_response["Meta Data"]["3. Last Refreshed"]
        break
    except:
        print("Hmm...it appears that you did not enter a valid symbol! Try again")

tsd = seg_response["Time Series (Daily)"]

dates = list(tsd.keys()) # TODO: Sort so latest day is first

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []
#maximum of all high prices
for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))


recent_high = max(high_prices)
recent_low = min(low_prices)


if float(latest_close) >= .6*recent_high and float(latest_close) <= .8*recent_high:
    buy_rec = "BUY!" 
    rec_reason = "STOCK PRICE IS BETWEEN 60% AND 80% OF RECENT HIGH."

else: 
    buy_rec = "DON'T BUY!"
    rec_reason = "PRICE IS NOT WITHIN THE ACCEPTABLE RANGE OF RECENT HIGH."

def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

#csv_file_path = "data/prices.csv" # a relative filepath

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    #looping
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
now = datetime.datetime.now()
print("REQUEST AT:", now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {buy_rec}")
print(f"RECOMMENDATION REASON: {rec_reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-----")