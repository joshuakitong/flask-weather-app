import os
import requests
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_key"  # Needed for flash()

API_KEY = os.getenv("API_KEY")

WEATHER_BACKGROUND_MAP = {
    "Clear": "sunny",
    "Clouds": "cloudy",
    "Rain": "rainy",
    "Drizzle": "rainy",
    "Thunderstorm": "stormy",
    "Snow": "snowy",
    "Mist": "foggy",
    "Fog": "foggy",
    "Haze": "foggy",
    "Smoke": "foggy",
    "Dust": "foggy",
    "Sand": "foggy",
    "Ash": "foggy",
    "Squall": "stormy",
    "Tornado": "stormy"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

            current_response = requests.get(current_url)
            forecast_response = requests.get(forecast_url)

            if current_response.status_code == 200 and forecast_response.status_code == 200:
                current_data = current_response.json()
                forecast_data = forecast_response.json()

                condition = current_data["weather"][0]["main"]

                hourly_forecast = [
                    {
                        "time": entry["dt_txt"],
                        "temp": entry["main"]["temp"],
                        "icon": entry["weather"][0]["icon"],
                        "description": entry["weather"][0]["description"]
                    }
                    for entry in forecast_data["list"][:6]
                ]

                daily_map = defaultdict(list)
                for entry in forecast_data["list"]:
                    date = entry["dt_txt"].split()[0]
                    daily_map[date].append(entry)

                daily_forecast = []
                for date, entries in list(daily_map.items())[:5]:
                    noon_entry = next((e for e in entries if "12:00:00" in e["dt_txt"]), entries[0])
                    daily_forecast.append({
                        "date": datetime.strptime(date, "%Y-%m-%d").strftime("%a, %b %d"),
                        "temp": noon_entry["main"]["temp"],
                        "icon": noon_entry["weather"][0]["icon"],
                        "description": noon_entry["weather"][0]["description"]
                    })

                return render_template("index.html",
                    weather={
                        "city": current_data["name"],
                        "temperature": current_data["main"]["temp"],
                        "feels_like": current_data["main"]["feels_like"],
                        "description": current_data["weather"][0]["description"],
                        "icon": current_data["weather"][0]["icon"]
                    },
                    background=WEATHER_BACKGROUND_MAP.get(condition, "default"),
                    hourly=hourly_forecast,
                    daily=daily_forecast
                )
            else:
                flash("City not found. Please try again.")
                return redirect(url_for("index"))
        else:
            flash("Please enter a city name.")
            return redirect(url_for("index"))

    return render_template("index.html", weather=None, background="default", hourly=None, daily=None)

if __name__ == "__main__":
    app.run(debug=True)
