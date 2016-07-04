import os
from flask import Flask
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from flask import make_response
from bson.json_util import dumps

APP_URL = os.environ.get('APP_URL')
if not APP_URL:
    APP_URL = 'http://localhost:5000'

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest"

app = Flask(__name__)

app.config['MONGO_URI'] = MONGO_URL
app.config['MONGO_DBNAME'] = "students_db"
mongo = PyMongo(app, config_prefix='MONGO')


def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

from application import resources
from application import views
