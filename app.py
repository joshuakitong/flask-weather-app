import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

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
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                condition = data["weather"][0]["main"]

                return redirect(url_for("index", 
                    city_name=data["name"],
                    temp=data["main"]["temp"],
                    feels_like= data["main"]["feels_like"],
                    desc=data["weather"][0]["description"],
                    icon=data["weather"][0]["icon"],
                    bg=WEATHER_BACKGROUND_MAP.get(condition, "default")
                ))
            else:
                flash("City not found. Please try again.")
                return redirect(url_for("index"))
        else:
            flash("Please enter a city name.")
            return redirect(url_for("index"))

    weather_data = None
    background = request.args.get("bg", "default")

    if "city_name" in request.args:
        weather_data = {
            "city": request.args.get("city_name"),
            "temperature": request.args.get("temp"),
            "feels_like": request.args.get("feels_like"),
            "description": request.args.get("desc"),
            "icon": request.args.get("icon")
        }

    return render_template("index.html", weather=weather_data, background=background)

if __name__ == "__main__":
    app.run(debug=True)