# Flask Weather App

This is a simple weather app built with **Python** and **Flask**, where users are able to search for the weather by city.

Live: [View Site](https://flask-weather-app-k7b3.onrender.com)

*Note: The app may take a few seconds to load as it’s hosted on Render.com’s free tier (services sleep when inactive).*

## Features

 - Search weather by city
 - Background changes base on weather condition

 <details>
  <summary><strong>How to Run Locally</strong></summary>

  1. Clone the repo  
     `git clone https://github.com/joshuakitong/flask-weather-app.git`

  2. Navigate to the project directory  
     `cd yourproject`

  3. (Optional) Create and activate a virtual environment  
     ```bash
     python -m venv venv
     # Windows:
     venv\Scripts\activate
     # macOS/Linux:
     source venv/bin/activate
     ```

  4. Install dependencies  
     `pip install -r requirements.txt`

  5. Create a `.env` file in the project root and add your OpenWeatherMap API key:  
     ```
     API_KEY=your_openweathermap_api_key
     ```

  6. Run the app  
     `python app.py`
</details>