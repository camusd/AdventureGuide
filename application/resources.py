from flask import jsonify, url_for, request, redirect
from flask_restful import Resource
from application import api, mongo, APP_URL
from bson.objectid import ObjectId
from .models import StudentModel


class Status(Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


class Student(Resource):
    def get(self, _id=None):
        data = StudentModel().getData(_id)
        return jsonify({"response": data})

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            mongo.db.student.insert_one(data)

    def put(self):
        data = request.get_json()
        key = data['_id']
        del data['_id']
        mongo.db.student.replace_one({"_id": ObjectId(key)}, data)

    def delete(self, _id):
        mongo.db.student.remove({'_id': ObjectId(_id)})


class MajorAttractions(Resource):
    def get(self, _id=None):
        if _id:
            data = mongo.db.majorAttractions.find_one({"_id": _id})
            if not data:
                response = jsonify({"message": "Major Attraction not found"})
                response.status_code = 404
                return response
            else:
                data["_id"] = str(data["_id"])
                response = jsonify(data)
                response.status_code = 200
                return response
        else:
            data = []
            cursor = mongo.db.majorAttractions.find()
            for attraction in cursor:
                attraction['_id'] = str(attraction['_id'])
                data.append(attraction)
            response = jsonify(data)
            response.status_code = 200
            return response

    def post(self):
        data = request.get_json()
        if not data:
            response = jsonify({"message": "Problems parsing JSON"})
            response.staus_code = 400
            return response
        elif not "name" in data or not "description" in data or \
            not "type" in data or not "details" in data or \
            not "location" in data:
            response = jsonify({"message:": "name, description, type, "
                + "details, and location are required fields"})
            response.status_code = 422
            return response
        else:
            _id = mongo.db.majorAttractions.insert_one(data)
            data['_id'] = str(data['_id'])
            response = jsonify(data)
            response.status_code = 201
            response.headers['Location'] = '/api/majorAttraction/' + \
                str(_id.inserted_id)
            return response

    def put(self, _id=None):
        if _id:
            data = request.get_json()
            if not data:
                response = jsonify({"message": "Expected data to be \
                    formated as JSON"})
                response.staus_code = 400
                return response
            elif not "name" in data or not "description" in data or \
                not "type" in data or not "details" in data or \
                not "location" in data:
                response = jsonify({"message:": "name, description, type, \
                    details, and location are required fields"})
                response.status_code = 422
                return response
            else:
                mongo.db.majorAttractions.replace_one({"_id": _id}, data)
                data['_id'] = str(_id)
                response = jsonify(data)
                response.status_code = 200
                return response
        else:
            response = jsonify({"message": "Not Found"})
            response.status_code = 404
            return response


    def delete(self, _id=None):
        if _id:
            data = mongo.db.majorAttractions.delete_one({"_id": _id})
            if not data.deleted_count:
                response = jsonify({"message": "Major Attraction not found"})
                response.status_code = 404
                return response
            else:
                return ('', 204)
        else:
            data = mongo.db.majorAttractions.delete_many({})
            return ('', 204)



api.add_resource(Status, '/status')
api.add_resource(Student, "/api", endpoint="students")
api.add_resource(Student, "/api/<string:_id>",
                 endpoint="student")
api.add_resource(MajorAttractions, "/api/majorAttractions",
                 endpoint="majorAttractions")
api.add_resource(MajorAttractions,
                 "/api/majorAttractions/<ObjectId:_id>",
                 endpoint="majorAttraction")
