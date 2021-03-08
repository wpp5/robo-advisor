# this is the "app/robo_advisor.py" file
# The code will take a ticket symbol from the user and return various information including a buy/don't buy reccomendation 

#Importing packages and modules
import os
import csv
import json
import datetime
import time
import sys


import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv


#Time delay to simulate computer thinking
delay = 1.5

#loads .env file
load_dotenv()

#variable assignmen for unique API key
apikey = os.environ.get("ALPHAVANTAGE_API_KEY")

#Data Validation for incorrect ticket entry
while True:
    symbol = input("Enter stock symbol for analysis. For example, AAPL, JNJ, etc.")
    if type(symbol) == str:
        if len(symbol) < 5:
            #Variable assignment to URL for ticker data
            request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}"
        else:
            again = input("Hmm..that doesn't appear to be a valid entry. Would you like to try again? Yes or No?").lower()
            if again == "yes":
                True
            else:
                print("Okay! Happy Investing!") 
                sys.exit()
    else:
        again = input("Hmm..that doesn't appear to be a valid entry. Would you like to try again? Yes or No?").lower()
        if again == "yes":
            True
        else:
            print("Okay! Happy Investing!")
            sys.exit()
  
    #Requests URL data
    response = requests.get(request_url)
    #Loads URL text
    seg_response = json.loads(response.text)
    #assigns variable to get into library
    try:
        tsd = seg_response["Time Series (Daily)"]
        break
    except:
        again = input("GHmm..that doesn't appear to be a valid entry. Would you like to try again? Yes or No?").lower()
        if again == "yes":
            True
        else:
            print("Okay! Happy Investing!")
            sys.exit()

#Assigns the dates into a list called dates
dates = list(tsd.keys())

#Sorts dates from most recent in case data format changes
dates.sort(reverse=True)

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []
closing_prices = []
#Loops from to find high and low prices for each day and appends them to the respective dictionaries
for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    closing_price = tsd[date]["4. close"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))
    closing_prices.append(float(closing_price))

#Returns high and low prices in the list
recent_high = max(high_prices)
recent_low = min(low_prices)

#Buy logic 
#Will recommend buy if latest close is between 60% and 80% of the recent high price
if float(latest_close) >= .6*recent_high and float(latest_close) <= .8*recent_high:
    buy_rec = "BUY!" 
    rec_reason = "STOCK PRICE IS BETWEEN 60% AND 80% OF RECENT HIGH."

#Will reccomend don't buy if the price does not meet the aforementioned conditions
else: 
    buy_rec = "DON'T BUY!"
    rec_reason = "PRICE IS NOT WITHIN THE ACCEPTABLE RANGE OF RECENT HIGH."

#to_usd converts non-formatted numbers to USD currency format
def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

#Puts the prices.csv file into the data folder in the robo-advisor repo
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
#Name of the headers for the CSV file
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

#Writes the values for the csv headers into the CSV file by looping through the days
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
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


##Info Outputs

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
time.sleep(delay)
#Uses the datatime function to return the current tume of the request
now = datetime.datetime.now()
print("REQUEST AT:", now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print(f"LATEST DAY: {latest_day}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {buy_rec}")
print(f"RECOMMENDATION REASON: {rec_reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
time.sleep(delay)
print("-------------------------")
print("HAPPY INVESTING!")
print("-----")

plt.plot(dates,closing_prices)
plt.title('Prices over time')
plt.xlabel('Time')
plt.ylabel('Closing Price')
plt.show()
