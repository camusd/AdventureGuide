from flask import render_template, jsonify, request
from application import app
from .models import StudentModel
import requests
import datetime


@app.route('/')
@app.route('/index')
def cloud():
    return render_template('index.html')


@app.route('/cloud')
def index():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    result1 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/conditions/q/OR/Corvallis.json')
    result2 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/forecast/q/OR/Corvallis.json')
    weather = result1.json()
    weather.update(result2.json())
    return render_template('cloud.html',
                           time=time,
                           weather=weather)


@app.route('/surveyResults')
def surveyResults():
    response = StudentModel().getData()
    return render_template('viewSurvey.html',
                           documents=response)


@app.route('/surveyResults/<object_id>')
def editSurveyResults(object_id):
    response = StudentModel().getData(object_id)
    return render_template('editSurvey.html',
                           document=response)
