from flask import render_template
from flask_rest_service import app
import requests
import datetime

@app.route('/')
@app.route('/index')
def index():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    # result1 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/conditions/q/OR/Corvallis.json')
    # result2 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/forecast/q/OR/Corvallis.json')
    # weather = result1.json()
    # weather.update(result2.json())
    return render_template('index.html',
                           time=time)
                        #    weather=weather)

  # <p>Current temp in Corvallis: {{ weather.current_observation.temp_f }}</p>
  # <p>Current weather in Corvallis: {{ weather.current_observation.weather}}</p>
  # <p>Current forecast for today in Corvallis: {{ weather.forecast.txt_forecast.forecastday[0].fcttext }}</p>
  # <img src="https://icons.wxug.com/logos/JPG/wundergroundLogo_4c_horz.jpg">
  # <footer><em>All weather data gathered from Weather Underground API</em></footer>
