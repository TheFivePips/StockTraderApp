import requests
from twilio.rest import Client
from dotenv import dotenv_values
from datetime import datetime, timedelta

config = dotenv_values(".env")

VIRTUAL_TWILIO_NUMBER = config["TWILIO_NUMBER"]
VERIFIED_NUMBER = config["MY_PHONE_NUMBER"]

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = config["ALPHA_API_KEY"]
NEWS_API_KEY = config["NEWS_API_KEY"]
TWILIO_SID = config["TWILIO_SSID"]
TWILIO_AUTH_TOKEN = config["TWILIO_TOKEN"]

yesterday = datetime.now() - timedelta(1)
day_before_yesterday = datetime.now() - timedelta(2)
yesterdays_date = datetime.strftime(yesterday, '%Y-%m-%d')
day_before_yesterdays_date = datetime.strftime(day_before_yesterday, '%Y-%m-%d')

#Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK_NAME,
    "interval": "30min",
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()
# print(data)

yesterdays_close_price = data['Time Series (30min)'][f"{yesterdays_date} 16:00:00"]["4. close"]

#Get the day before yesterday's closing stock price
day_before_yesterdays_close_price = data['Time Series (30min)'][f"{day_before_yesterdays_date} 16:00:00"]["4. close"]

difference = abs(float(yesterdays_close_price) - float(day_before_yesterdays_close_price))
# calc % difference
diff_percent = (difference / float(yesterdays_close_price)) * 100

if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in three_articles:
        # print(article)
        message = client.messages.create(
            body=article["title"],
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
