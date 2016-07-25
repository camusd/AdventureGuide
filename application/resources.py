from flask import jsonify, url_for, request, redirect, abort
from flask_restful import Resource, reqparse
from application import api, APP_URL
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from . import models
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MajorAttractions(Resource):
    def __init__(self):
        self.root_parser = reqparse.RequestParser()
        self.root_parser.add_argument('name', type=str, required=True,
            location='json',
            help="Missing name string parameter in the JSON body")
        self.root_parser.add_argument('description', type=str,
            required=True, location='json',
            help="Missing description string parameter in the JSON body")
        self.root_parser.add_argument('details', type=dict,
            location='json',
            help="Missing details embedded JSON object in the JSON body")
        self.root_parser.add_argument('location', type=dict,
            location='json',
            help="Missing location embedded JSON object in the JSON body")
        self.location_parser = reqparse.RequestParser()
        self.location_parser.add_argument('type', type=str,
            required=True, location='location',
            help="Missing type string parameter in the embedded location JSON object in the JSON body")
        self.location_parser.add_argument('coordinates', type=list,
            required=True, location='location',
            help="Missing coordinates longitude and latitude tuple in the embedded location JSON object in the JSON body")
        super(MajorAttractions, self).__init__()

    def get(self, _id=None):
        if _id:
            majorAttraction = models.MajorAttraction.objects.get_or_404(id=_id)
            json = loads(majorAttraction.to_json())
            json = JSONEncoder().encode(json)
            response = jsonify(loads(json))
            response.status_code = 200
            return response
        else:
            data = []
            cursor = models.MajorAttraction.objects.all()
            for attraction in cursor:
                json = loads(attraction.to_json())
                json = JSONEncoder().encode(json)
                data.append(loads(json))
            response = jsonify(data)
            response.status_code = 200
            return response

    def post(self):
        data = request.get_json()
        if not data:
            abort(400)
        root_args = self.root_parser.parse_args()
        location_args = self.location_parser.parse_args(req=root_args)
        majorAttraction = models.MajorAttraction(**data)
        majorAttraction.save()
        majorAttraction.url = APP_URL + "/api/majorAttraction/" + \
            str(majorAttraction.id)
        majorAttraction.save()
        json = loads(majorAttraction.to_json())
        json = JSONEncoder().encode(json)
        response = jsonify(loads(json))
        response.status_code = 201
        response.headers['Location'] = '/api/majorAttraction/' + \
            str(majorAttraction.id)
        return response

    def put(self, _id=None):
        if _id:
            data = request.get_json()
            if not data:
                abort(400)
            root_args = self.root_parser.parse_args()
            location_args = self.location_parser.parse_args(req=root_args)
            majorAttraction = models.MajorAttraction.objects.get_or_404(id=_id)
            majorAttraction.update(**data)
            majorAttraction = models.MajorAttraction.objects.get_or_404(id=_id)
            json = loads(majorAttraction.to_json())
            json = JSONEncoder().encode(json)
            response = jsonify(loads(json))
            response.status_code = 200
            return response
        else:
            abort(404)

    def delete(self, _id=None):
        if _id:
            majorAttraction = models.MajorAttraction.objects.get_or_404(id=_id)
            majorAttraction.delete()
            return ('', 204)
        else:
            cursor = models.MajorAttraction.objects.all()
            for attraction in cursor:
                attraction.delete()
            return ('', 204)


api.add_resource(MajorAttractions, "/api/majorAttractions",
                 endpoint="majorAttractions")
api.add_resource(MajorAttractions,
                 "/api/majorAttractions/<string:_id>",
                 endpoint="majorAttraction")


class MinorAttractions(Resource):
    def __init__(self):
        self.root_parser = reqparse.RequestParser()
        self.root_parser.add_argument('name', type=str, required=True,
            location='json',
            help="Missing name string parameter in the JSON body")
        self.root_parser.add_argument('description', type=str,
            required=True, location='json',
            help="Missing description string parameter in the JSON body")
        self.root_parser.add_argument('majorAttraction', type=ObjectId,
            required=True, location='json',
            help="Missing parent Major Attraction ObjectId in the JSON body")
        self.root_parser.add_argument('details', type=dict,
            location='json',
            help="Missing details embedded JSON object in the JSON body")
        self.root_parser.add_argument('location', type=dict,
            location='json',
            help="Missing location embedded JSON object in the JSON body")
        self.location_parser = reqparse.RequestParser()
        self.location_parser.add_argument('type', type=str,
            required=True, location='location',
            help="Missing type string parameter in the embedded location JSON object in the JSON body. Value must be 'Point'")
        self.location_parser.add_argument('coordinates', type=list,
            required=True, location='location',
            help="Missing coordinates longitude and latitude tuple in the embedded location JSON object in the JSON body")
        super(MinorAttractions, self).__init__()

    def get(self, _id=None):
        if _id:
            minorAttraction = models.MinorAttraction.objects.get_or_404(id=_id)
            json = loads(minorAttraction.to_json())
            json['majorAttraction'] = loads(
                minorAttraction.majorAttraction.to_json())
            json = JSONEncoder().encode(json)
            response = jsonify(loads(json))
            response.status_code = 200
            return response
        else:
            data = []
            cursor = models.MinorAttraction.objects.all()
            for attraction in cursor:
                json = loads(attraction.to_json())
                json['majorAttraction'] = loads(
                    attraction.majorAttraction.to_json())
                json = JSONEncoder().encode(json)
                data.append(loads(json))
            response = jsonify(data)
            response.status_code = 200
            return response

    def post(self):
        data = request.get_json()
        if not data:
            abort(400)
        root_args = self.root_parser.parse_args()
        location_args = self.location_parser.parse_args(req=root_args)
        majorAttraction = models.MajorAttraction.objects.get_or_404(
            id=data['majorAttraction'])
        data['majorAttraction'] = majorAttraction
        minorAttraction = models.MinorAttraction(**data)
        minorAttraction.save()
        minorAttraction.url = APP_URL + "/api/majorAttraction/" + \
            str(minorAttraction.id)
        minorAttraction.save()
        json = loads(minorAttraction.to_json())
        json['majorAttraction'] = loads(majorAttraction.to_json())
        json = JSONEncoder().encode(json)
        response = jsonify(loads(json))
        response.status_code = 201
        response.headers['Location'] = '/api/minorAttraction/' + \
            str(minorAttraction.id)
        return response

    def put(self, _id=None):
        if _id:
            data = request.get_json()
            if not data:
                abort(400)
            root_args = self.root_parser.parse_args()
            location_args = self.location_parser.parse_args(req=root_args)
            minorAttraction = models.MinorAttraction.objects.get_or_404(id=_id)
            majorAttraction = models.MajorAttraction.objects.get_or_404(
                id=data['majorAttraction'])
            data['majorAttraction'] = majorAttraction
            minorAttraction.update(**data)
            minorAttraction = models.MinorAttraction.objects.get_or_404(id=_id)
            json = loads(minorAttraction.to_json())
            json['majorAttraction'] = loads(majorAttraction.to_json())
            json = JSONEncoder().encode(json)
            response = jsonify(loads(json))
            response.status_code = 200
            return response
        else:
            abort(404)

    def delete(self, _id=None):
        if _id:
            minorAttraction = models.MinorAttraction.objects.get_or_404(id=_id)
            minorAttraction.delete()
            return ('', 204)
        else:
            cursor = models.MinorAttraction.objects.all()
            for attraction in cursor:
                attraction.delete()
            return ('', 204)


api.add_resource(MinorAttractions, "/api/minorAttractions",
                 endpoint="minorAttractions")
api.add_resource(MinorAttractions,
                 "/api/minorAttractions/<string:_id>",
                 endpoint="minorAttraction")
