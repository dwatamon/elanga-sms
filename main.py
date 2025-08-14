from flask import Flask, request
from datetime import datetime
import requests
import os
from twilio.rest import Client
import csv

app = Flask(__name__)

OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

FARMER_FILE = "farmers.csv"
MARKET_FILE = "market_prices.csv"

def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    res = requests.get(url).json()
    if res.get("cod") != 200:
        return "Weather data unavailable"
    temp = res["main"]["temp"]
    description = res["weather"][0]["description"].capitalize()
    return f"{temp:.1f}°C, {description}"

def get_market_prices():
    prices = []
    with open(MARKET_FILE, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) == 2:
                commodity, price = row
                prices.append(f"{commodity}: {price} CDF/kg")
    return "; ".join(prices)

def send_sms(to, message):
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to
    )

@app.route("/send_updates", methods=["GET"])
def send_updates():
    with open(FARMER_FILE, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) == 2:
                phone, location = row
                weather = get_weather(location)
                market = get_market_prices()
                message = f"Bonjour! Meteo aujourd'hui à {location}: {weather}. Prix: {market}."
                send_sms(phone, message)
    return "Updates sent", 200

if __name__ == '__main__':
    app.run(debug=True)
