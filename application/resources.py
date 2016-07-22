from flask import jsonify, url_for, request, redirect, abort
from flask_restful import Resource, reqparse
from application import api
from bson.objectid import ObjectId
from . import models


class MajorAttractions(Resource):
    def __init__(self):
        self.root_parser = reqparse.RequestParser()
        self.root_parser.add_argument('name', type=str, required=True,
            location='json')
        self.root_parser.add_argument('description', type=str,
            required=True, location='json')
        self.root_parser.add_argument('details', type=dict,
            location='json')
        self.root_parser.add_argument('location', type=dict,
            location='json')
        self.location_parser = reqparse.RequestParser()
        self.location_parser.add_argument('type', type=str,
            required=True, location='location')
        self.location_parser.add_argument('coordinates', type=list,
            required=True, location='location')
        super(MajorAttractions, self).__init__()

    def get(self, _id=None):
        if _id:
            MajorAttraction = models.MajorAttraction.objects.get_or_404(id=_id)
            response = jsonify(MajorAttraction)
            response.status_code = 200
            return response
        else:
            data = []
            cursor = models.MajorAttraction.objects.all()
            for attraction in cursor:
                data.append(attraction)
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
        response = jsonify(majorAttraction)
        response.status_code = 201
        response.headers['Location'] = '/api/majorAttraction/' + \
            str(majorAttraction.id)
        return response

    def put(self, _id=None):
        if _id:
            data = request.get_json()
            if not data:
                abort(400)
            if data['_id']:
                del data['_id']
            root_args = self.root_parser.parse_args()
            location_args = self.location_parser.parse_args(req=root_args)
            majorAttraction = models.MajorAttraction.objects.get_or_404(id=_id)
            majorAttraction.update(**data)
            majorAttraction = models.MajorAttraction.objects.get_or_404(id=_id)
            response = jsonify(majorAttraction)
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "Not Found"})
            response.status_code = 404
            return response

    def delete(self, _id=None):
        if _id:
            majorAttraction = models.MajorAttraction.objects.get_of_404(id=_id)
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
