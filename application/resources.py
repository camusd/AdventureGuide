from flask import jsonify, url_for, request, redirect, abort
from flask_restful import Resource, reqparse
from application import APP_URL
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from . import models
from datetime import datetime
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
            location='json', trim=True,
            help="Missing name string parameter in the JSON body")
        self.root_parser.add_argument('description', type=str,
            required=True, location='json', trim=True,
            help="Missing description string parameter in the JSON body")
        self.root_parser.add_argument('details', type=dict,
            location='json',
            help="Missing details embedded JSON object in the JSON body")
        self.root_parser.add_argument('location', type=dict,
            location='json',
            help="Missing location embedded JSON object in the JSON body")

        self.location_parser = reqparse.RequestParser()
        self.location_parser.add_argument('type', type=str,
            required=True, location='location', trim=True,
            help="Missing type string parameter in the embedded location JSON object in the JSON body")
        self.location_parser.add_argument('coordinates', type=list,
            required=True, location='location',
            help="Missing coordinates longitude and latitude tuple in the embedded location JSON object in the JSON body")

        self.details_parser = reqparse.RequestParser()
        self.details_parser.add_argument('catagory', type=str,
            location='details', trim=True,
            help="")
        self.details_parser.add_argument('fee', type=float,
            location='details',
            help="")
        self.details_parser.add_argument('elevation', type=str,
            location='details', trim=True,
            help="")
        self.details_parser.add_argument('size', type=str,
            location='details', trim=True,
            help="")

        super(MajorAttractions, self).__init__()

    def get(self, _id=None, reviews=None):
        if _id:
            if reviews:
                if reviews == 'reviews':
                    data = []
                    cursor = models.Review.objects(attraction=_id)
                    for review in cursor:
                        json = loads(review.to_json())
                        json['attraction_url'] = review.attraction.url
                        json['user_url'] = review.user.url
                        json['user_history_url'] = review.user.history_url
                        json['timestamp'] = json['timestamp'].strftime(
                            '%Y-%m-%dT%H:%M:%SZ')
                        json = JSONEncoder().encode(json)
                        data.append(loads(json))
                    response = jsonify(data)
                    response.status_code = 200
                    return response
                else:
                    abort(400)
            else:
                majorAttraction = models.MajorAttraction.objects.get_or_404(
                    id=_id)
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
        if(data['location']):
            location_args = self.location_parser.parse_args(req=root_args)
        if(data['details']):
            details_args = self.details_parser.parse_args(req=root_args)
        attractionDetails = models.AttractionDetails(**data['details'])
        data['details'] = attractionDetails
        majorAttraction = models.MajorAttraction(**data)
        majorAttraction.save()
        majorAttraction.url = APP_URL + "/api/majorAttractions/" + \
            str(majorAttraction.id)
        majorAttraction.reviews_url = APP_URL + "/api/majorAttractions/" + \
            str(majorAttraction.id) + "/reviews"
        majorAttraction.save()
        json = loads(majorAttraction.to_json())
        json = JSONEncoder().encode(json)
        response = jsonify(loads(json))
        response.status_code = 201
        response.headers['Location'] = '/api/majorAttractions/' + \
            str(majorAttraction.id)
        return response

    def put(self, _id=None, reviews=None):
        if reviews:
            abort(400)
        if _id:
            data = request.get_json()
            if not data:
                abort(400)
            root_args = self.root_parser.parse_args()
            if(data['location']):
                location_args = self.location_parser.parse_args(req=root_args)
            if(data['details']):
                details_args = self.details_parser.parse_args(req=root_args)
            majorAttraction = models.MajorAttraction.objects.get_or_404(id=_id)
            majorAttraction.update(**data)
            majorAttraction = models.MajorAttraction.objects.get_or_404(id=_id)
            json = loads(majorAttraction.to_json())
            json = JSONEncoder().encode(json)
            response = jsonify(loads(json))
            response.status_code = 200
            return response
        else:
            abort(400)

    def delete(self, _id=None, reviews=None):
        if _id:
            if reviews:
                attraction = models.MajorAttraction.objects.get_or_404(id=_id)
                cursor = models.Review.objects(attraction=attraction)
                for review in cursor:
                    review.attraction.dec_reviews()
                    review.attraction.save()
                    review.delete()
                return ('', 204)
            else:
                majorAttraction = \
                    models.MajorAttraction.objects.get_or_404(id=_id)
                majorAttraction.delete()
                return ('', 204)
        else:
            cursor = models.MajorAttraction.objects.all()
            for attraction in cursor:
                attraction.delete()
            return ('', 204)


class MinorAttractions(Resource):
    def __init__(self):
        self.root_parser = reqparse.RequestParser()
        self.root_parser.add_argument('name', type=str, required=True,
            location='json', trim=True,
            help="Missing name string parameter in the JSON body")
        self.root_parser.add_argument('description', type=str,
            required=True, location='json', trim=True,
            help="Missing description string parameter in the JSON body")
        self.root_parser.add_argument('majorAttraction', type=ObjectId,
            required=True, location='json', trim=True,
            help="Missing parent majorAttraction ObjectId parameter in the JSON body")
        self.root_parser.add_argument('details', type=dict,
            location='json',
            help="Missing details embedded JSON object in the JSON body")
        self.root_parser.add_argument('location', type=dict,
            location='json',
            help="Missing location embedded JSON object in the JSON body")

        self.location_parser = reqparse.RequestParser()
        self.location_parser.add_argument('type', type=str,
            required=True, location='location', trim=True,
            help="Missing type string parameter in the embedded location JSON object in the JSON body. Value must be 'Point'")
        self.location_parser.add_argument('coordinates', type=list,
            required=True, location='location',
            help="Missing coordinates longitude and latitude tuple in the embedded location JSON object in the JSON body")

        self.details_parser = reqparse.RequestParser()
        self.details_parser.add_argument('catagory', type=str,
            location='details', trim=True,
            help="")
        self.details_parser.add_argument('fee', type=float,
            location='details',
            help="")
        self.details_parser.add_argument('elevation', type=str,
            location='details', trim=True,
            help="")
        self.details_parser.add_argument('size', type=str,
            location='details', trim=True,
            help="")

        super(MinorAttractions, self).__init__()

    def get(self, _id=None, reviews=None):
        if _id:
            if reviews:
                if reviews == 'reviews':
                    data = []
                    minorAttraction = \
                        models.MinorAttraction.objects.get_or_404(id=_id)
                    cursor = models.Review.objects(
                        attraction=minorAttraction)
                    for review in cursor:
                        json = loads(review.to_json())
                        json['attraction_url'] = review.attraction.url
                        json['user_url'] = review.user.url
                        json['user_history_url'] = review.user.history_url
                        json['timestamp'] = json['timestamp'].strftime(
                            '%Y-%m-%dT%H:%M:%SZ')
                        json = JSONEncoder().encode(json)
                        data.append(loads(json))
                    response = jsonify(data)
                    response.status_code = 200
                    return response
                else:
                    abort(400)
            else:
                minorAttraction = \
                    models.MinorAttraction.objects.get_or_404(id=_id)
                json = loads(minorAttraction.to_json())
                json['majorAttraction_url'] = \
                    minorAttraction.majorAttraction.url
                json = JSONEncoder().encode(json)
                response = jsonify(loads(json))
                response.status_code = 200
                return response
        else:
            data = []
            cursor = models.MinorAttraction.objects.all()
            for attraction in cursor:
                json = loads(attraction.to_json())
                json['majorAttraction_url'] = \
                    attraction.majorAttraction.url
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
        if(data['location']):
            location_args = self.location_parser.parse_args(req=root_args)
        if(data['details']):
            details_args = self.details_parser.parse_args(req=root_args)
        majorAttraction = models.MajorAttraction.objects.get_or_404(
            id=data['majorAttraction'])
        data['majorAttraction'] = majorAttraction
        attractionDetails = models.AttractionDetails(**data['details'])
        data['details'] = attractionDetails
        minorAttraction = models.MinorAttraction(**data)
        minorAttraction.save()
        minorAttraction.url = APP_URL + "/api/minorAttractions/" + \
            str(minorAttraction.id)
        minorAttraction.reviews_url = \
            APP_URL + "/api/minorAttractions/" + \
            str(minorAttraction.id) + "/reviews"
        minorAttraction.save()
        json = loads(minorAttraction.to_json())
        json['majorAttraction_url'] = minorAttraction.majorAttraction.url
        json = JSONEncoder().encode(json)
        response = jsonify(loads(json))
        response.status_code = 201
        response.headers['Location'] = '/api/minorAttractions/' + \
            str(minorAttraction.id)
        return response

    def put(self, _id=None, reviews=None):
        if reviews:
            abort(400)
        if _id:
            data = request.get_json()
            if not data:
                abort(400)
            root_args = self.root_parser.parse_args()
            if(data['location']):
                location_args = \
                    self.location_parser.parse_args(req=root_args)
            if(data['details']):
                details_args = \
                    self.details_parser.parse_args(req=root_args)
            minorAttraction = \
                models.MinorAttraction.objects.get_or_404(id=_id)
            majorAttraction = models.MajorAttraction.objects.get_or_404(
                id=data['majorAttraction'])
            data['majorAttraction'] = majorAttraction
            minorAttraction.update(**data)
            minorAttraction = \
                models.MinorAttraction.objects.get_or_404(id=_id)
            json = loads(minorAttraction.to_json())
            json['majorAttraction_url'] = \
                minorAttraction.majorAttraction.url
            json = JSONEncoder().encode(json)
            response = jsonify(loads(json))
            response.status_code = 200
            return response
        else:
            abort(400)

    def delete(self, _id=None, reviews=None):
        if _id:
            if reviews:
                attraction = models.MinorAttraction.objects.get_or_404(id=_id)
                cursor = models.Review.objects(attraction=attraction)
                for review in cursor:
                    review.attraction.dec_reviews()
                    review.attraction.save()
                    review.delete()
                return ('', 204)
            else:
                minorAttraction = \
                    models.MinorAttraction.objects.get_or_404(id=_id)
                minorAttraction.delete()
                return ('', 204)
        else:
            cursor = models.MinorAttraction.objects.all()
            for attraction in cursor:
                attraction.delete()
            return ('', 204)


class Users(Resource):
    def __init__(self):
        self.root_parser = reqparse.RequestParser()
        self.root_parser.add_argument('firstname', type=str, required=True,
            location='json', trim=True,
            help="Missing firstname string parameter in the JSON body")
        self.root_parser.add_argument('lastname', type=str, required=True,
            location='json', trim=True,
            help="Missing lastname string parameter in the JSON body")
        self.root_parser.add_argument('username', type=str, required=True,
            location='json', trim=True,
            help="Missing username string parameter in the JSON body")
        self.root_parser.add_argument('password', type=str,
            required=True, location='json', trim=True,
            help="Missing password string parameter in the JSON body")
        self.root_parser.add_argument('email', type=str,
            required=True, location='json', trim=True,
            help="Missing email string parameter in the JSON body")
        self.root_parser.add_argument('admin', type=str,
            location='json',
            help="")

        super(Users, self).__init__()

    def get(self, _id=None, history=None):
        if _id:
            if history:
                if history == 'history':
                    data = []
                    cursor = models.Review.objects(user=_id)
                    for review in cursor:
                        json = loads(review.to_json())
                        json['attraction_url'] = review.attraction.url
                        json['attraction_reviews_url'] = \
                            review.attraction.reviews_url
                        json['user_url'] = review.user.url
                        json['timestamp'] = json['timestamp'].strftime(
                            '%Y-%m-%dT%H:%M:%SZ')
                        json = JSONEncoder().encode(json)
                        data.append(loads(json))
                    response = jsonify(data)
                    response.status_code = 200
                    return response
                else:
                    abort(400)
            else:
                user = models.User.objects.get_or_404(id=_id)
                json = loads(user.to_json())
                json['timestamp'] = json['timestamp'].strftime(
                    '%Y-%m-%dT%H:%M:%SZ')
                json = JSONEncoder().encode(json)
                response = jsonify(loads(json))
                response.status_code = 200
                return response
        else:
            data = []
            cursor = models.User.objects.all()
            for user in cursor:
                json = loads(user.to_json())
                json['timestamp'] = json['timestamp'].strftime(
                    '%Y-%m-%dT%H:%M:%SZ')
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
        if data['admin'] == "true":
            data['admin'] = True
        else:
            data['admin'] = False
        user = models.User(**data)
        user.save()
        user.url = APP_URL + "/api/users/" + \
            str(user.id)
        user.history_url = APP_URL + "/api/users/" + \
            str(user.id) + "/history"
        user.save()
        json = loads(user.to_json())
        json['timestamp'] = json['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ')
        json = JSONEncoder().encode(json)
        response = jsonify(loads(json))
        response.status_code = 201
        response.headers['Location'] = '/api/users/' + \
            str(user.id)
        return response

    def put(self, _id=None, history=None):
        if history:
            abort(400)
        if _id:
            data = request.get_json()
            if not data:
                abort(400)
            root_args = self.root_parser.parse_args()
            if data['admin'] == "true":
                data['admin'] = True
            else:
                data['admin'] = False
            user = models.User.objects.get_or_404(id=_id)
            user.update(**data)
            user = models.User.objects.get_or_404(id=_id)
            json = loads(user.to_json())
            json['timestamp'] = json['timestamp'].strftime(
                '%Y-%m-%dT%H:%M:%SZ')
            json = JSONEncoder().encode(json)
            response = jsonify(loads(json))
            response.status_code = 200
            return response
        else:
            abort(400)

    def delete(self, _id=None, history=None):
        if _id:
            if history:
                user = models.User.objects.get_or_404(id=_id)
                cursor = models.Review.objects(user=user)
                for review in cursor:
                    review.attraction.dec_reviews()
                    review.attraction.save()
                    review.delete()
                return ('', 204)
            else:
                user = models.User.objects.get_or_404(id=_id)
                user.delete()
                return ('', 204)
        else:
            cursor = models.User.objects.all()
            for user in cursor:
                user.delete()
            return ('', 204)


class Reviews(Resource):
    def __init__(self):
        self.root_parser = reqparse.RequestParser()
        self.root_parser.add_argument('attraction',
            type=ObjectId, required=True, location='json', trim=True,
            help="Missing parent attraction ObjectId parameter in the JSON body")
        self.root_parser.add_argument('body', type=str,
            required=True, location='json', trim=True,
            help="Missing body string parameter in the JSON body")

        super(Reviews, self).__init__()

    def get(self, _id=None, upvote=None):
        if upvote:
            abort(400)
        if _id:
            review = models.Review.objects.get_or_404(id=_id)
            json = loads(review.to_json())
            json['attraction_url'] = review.attraction.url
            json['attraction_reviews_url'] = review.attraction.reviews_url
            json['user_url'] = review.user.url
            json['user_history_url'] = review.user.history_url
            json['timestamp'] = json['timestamp'].strftime(
                '%Y-%m-%dT%H:%M:%SZ')
            json = JSONEncoder().encode(json)
            response = jsonify(loads(json))
            response.status_code = 200
            return response
        else:
            abort(400)

    def post(self, _id=None, upvote=None):
        if upvote:
            abort(400)
        if _id:
            data = request.get_json()
            if not data:
                abort(400)
            root_args = self.root_parser.parse_args()
            user = models.User.objects.get_or_404(id=_id)
            data['user'] = user
            attraction = models.Attraction.objects.get_or_404(
                id=data['attraction'])
            attraction.inc_reviews()
            attraction.save()
            data['attraction'] = attraction
            review = models.Review(**data)
            review.save()
            review.url = APP_URL + "/api/reviews/" + \
                str(review.id)
            review.upvote_url = APP_URL + "/api/reviews/" + \
                str(review.id) + "/upvote"
            review.save()
            json = loads(review.to_json())
            json['attraction_url'] = review.attraction.url
            json['attraction_reviews_url'] = review.attraction.reviews_url
            json['user_url'] = review.user.url
            json['user_history_url'] = review.user.history_url
            json['timestamp'] = json['timestamp'].strftime(
                '%Y-%m-%dT%H:%M:%SZ')
            json = JSONEncoder().encode(json)
            response = jsonify(loads(json))
            response.status_code = 201
            response.headers['Location'] = '/api/reviews/' + \
                str(review.id)
            return response
        else:
            abort(400)

    def put(self, _id=None, upvote=None):
        if _id:
            if upvote:
                if upvote == "upvote":
                    review = models.Review.objects.get_or_404(id=_id)
                    review.inc_upvotes()
                    review.save()
                    return ('', 204)
                else:
                    abort(400)
            else:
                data = request.get_json()
                if not data:
                    abort(400)
                root_args = self.root_parser.parse_args()
                user = models.User.objects.get_or_404(
                    id=data['user'])
                data['user'] = user
                attraction = models.Attraction.objects.get_or_404(
                    id=data['attraction'])
                data['attraction'] = attraction
                review = models.Review.objects.get_or_404(id=_id)
                review.update(**data)
                review = models.Review.objects.get_or_404(id=_id)
                json = loads(review.to_json())
                json['attraction_url'] = review.attraction.url
                json['attraction_reviews_url'] = review.attraction.reviews_url
                json['user_url'] = review.user.url
                json['user_history_url'] = review.user.history_url
                json['timestamp'] = json['timestamp'].strftime(
                    '%Y-%m-%dT%H:%M:%SZ')
                json = JSONEncoder().encode(json)
                response = jsonify(loads(json))
                response.status_code = 200
                return response
        else:
            abort(400)

    def delete(self, _id=None, upvote=None):
        if _id:
            if upvote:
                if upvote == "upvote":
                    review = models.Review.objects.get_or_404(id=_id)
                    review.dec_upvotes()
                    review.save()
                    return ('', 204)
                else:
                    abort(400)
            else:
                review = models.Review.objects.get_or_404(id=_id)
                review.attraction.dec_reviews()
                review.attraction.save()
                review.delete()
                return ('', 204)
        else:
            abort(400)
