import requests
from dotenv import dotenv_values
from datetime import datetime, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
url = "https://www.alphavantage.co/query?"
config = dotenv_values(".env")
yesterday = datetime.now() - timedelta(1)
day_before_yesterday = datetime.now() - timedelta(2)
yesterdays_date = datetime.strftime(yesterday, '%Y-%m-%d')
day_before_yesterdays_date = datetime.strftime(day_before_yesterday, '%Y-%m-%d')

# print(yesterdays_date)


stock_params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "30min",
    "apikey": config["API_KEY"]
}

response = requests.get(url, params=stock_params)
data = response.json()

yesterdays_close_price = data["Time Series (30min)"][f"{yesterdays_date} 16:00:00"]["4. close"]
day_before_yesterdays_close_price = data["Time Series (30min)"][f"{day_before_yesterdays_date} 16:00:00"]["4. close"]

difference = abs(float(yesterdays_close_price) - float(day_before_yesterdays_close_price))

diff_percent = (difference / float(yesterdays_close_price)) * 100
print(diff_percent)

if diff_percent > 1:
    news_url = "https://newsapi.org/v2/everything?"
    news_params = {
        "apiKey": config["NEWS_API_KEY"],
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(news_url, params=news_params)
    news_data = news_response.json()["articles"]
    top_three_articles = news_data[:3]
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
