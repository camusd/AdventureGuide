from flask import Flask
import requests
import datetime

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# print the time of day in Corvallis.
def timeofday():
    now = datetime.datetime.now()
    return '<p>Current time on AWS EC2 Instance: %s</p>\n' % now.strftime("%H:%M:%S")

# print weather conditions and forecast in Corvallis.
def weather():
    result1 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/conditions/q/OR/Corvallis.json')
    result2 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/forecast/q/OR/Corvallis.json')
    weather = result1.json()
    weather.update(result2.json())
    return '<p>Current temp in Corvallis: %d</p>\n \
        <p>Current weather in Corvallis: %s</p>\n \
        <p>Current forecast for today in Corvallis: %s</p>\n' \
        % (weather['current_observation']['temp_f'], weather['current_observation']['weather'], weather['forecast']['txt_forecast']['forecastday'][1]['fcttext'])

# some bits of text for the page.
header_text = '''<html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''<p><em>Hint</em>: This is a RESTful web service! Append a
    username to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific </p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
wunderground_logo = '<img src="https://icons.wxug.com/logos/JPG/wundergroundLogo_4c_horz.jpg">'
wunderground_credit = '<footer>All weather data is gathered using Weather Underground API</footer>'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + timeofday() + weather() + instructions + wunderground_logo + wunderground_credit + footer_text))

# add a rule when the page is accessed with a name appended to the site URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run()
