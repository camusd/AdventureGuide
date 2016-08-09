import os
from flask import Flask, make_response
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
from bson.json_util import dumps

APP_URL = os.environ.get('APP_URL')
# if not APP_URL:
    # APP_URL = 'http://localhost:5000'
    # APP_URL =

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest"

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = "KeepThisS3cr3t!!@"

app = Flask(__name__)

# app.config['MONGODB_SETTINGS'] = {'db': 'helloCloud', 'host': MONGO_URL}
app.config['MONGODB_SETTINGS'] = {
    'db': 'helloCloud',
    'username': 'ec2-user',
    'host': 'ec2-52-37-96-153.us-west-2.compute.amazonaws.com',
    'port': 27017
}
app.config['SECRET_KEY'] = SECRET_KEY
mongo = MongoEngine(app)


def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

def register_resources(api):
    from application.resources import (MajorAttractions,
                                       MinorAttractions,
                                       Users,
                                       Reviews)
    api.add_resource(MajorAttractions,
                     "/api/majorAttractions/<string:_id>/<string:reviews>",
                     endpoint="majorAttraction_reviews")
    api.add_resource(MajorAttractions,
                     "/api/majorAttractions/<string:_id>",
                     endpoint="majorAttraction")
    api.add_resource(MajorAttractions, "/api/majorAttractions",
                     endpoint="majorAttractions")
    api.add_resource(MinorAttractions,
                     "/api/minorAttractions/<string:_id>/<string:reviews>",
                     endpoint="minorAttraction_reviews")
    api.add_resource(MinorAttractions,
                     "/api/minorAttractions/<string:_id>",
                     endpoint="minorAttraction")
    api.add_resource(MinorAttractions, "/api/minorAttractions",
                     endpoint="minorAttractions")
    api.add_resource(Users,
                     "/api/users/<string:_id>/<string:history>",
                     endpoint="user_history")
    api.add_resource(Users,
                     "/api/users/<string:_id>",
                     endpoint="user")
    api.add_resource(Users, "/api/users",
                     endpoint="users")
    api.add_resource(Reviews,
                     "/api/reviews/<string:_id>/<string:upvote>",
                     endpoint="upvote_review")
    api.add_resource(Reviews,
                     "/api/reviews/<string:_id>",
                     endpoint="review")
    api.add_resource(Reviews, "/api/reviews",
                     endpoint="reviews")

register_resources(api)

def register_blueprints(app):
    from application.views import surveys, cloud, howto
    app.register_blueprint(surveys)
    app.register_blueprint(cloud)
    app.register_blueprint(howto)

register_blueprints(app)
