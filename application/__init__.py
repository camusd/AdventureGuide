import os
from flask import Flask, make_response
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
from bson.json_util import dumps

APP_URL = os.environ.get('APP_URL')
if not APP_URL:
    APP_URL = 'http://localhost:5000'

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest"

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = "KeepThisS3cr3t!!@"

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {'DB': 'helloCloud', 'host': MONGO_URL}
app.config['SECRET_KEY'] = SECRET_KEY
mongo = MongoEngine(app)


def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

def register_resources():
    from application.resources import MajorAttractions
    from application.resources import MinorAttractions
    api.add_resource(MajorAttractions, "/api/majorAttractions",
                     endpoint="majorAttractions")
    api.add_resource(MajorAttractions,
                     "/api/majorAttractions/<string:_id>",
                     endpoint="majorAttraction")
    api.add_resource(MinorAttractions, "/api/minorAttractions",
                     endpoint="minorAttractions")
    api.add_resource(MinorAttractions,
                     "/api/minorAttractions/<string:_id>",
                     endpoint="minorAttraction")

register_resources()

def register_blueprints(app):
    from application.views import surveys
    from application.views import cloud
    app.register_blueprint(surveys)
    app.register_blueprint(cloud)

register_blueprints(app)
