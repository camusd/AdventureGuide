from flask import render_template
from flask_rest_service import app
import requests
import datetime

@app.route('/')
@app.route('/index')
def index():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    result1 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/conditions/q/OR/Corvallis.json')
    result2 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/forecast/q/OR/Corvallis.json')
    weather = result1.json()
    weather.update(result2.json())
    return render_template('index.html',
                           time=time,
                           weather=weather)
