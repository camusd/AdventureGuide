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
    def get(self, object_id=None):
        data = StudentModel().getData()
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


api.add_resource(Status, '/status')
api.add_resource(Student, "/api", endpoint="students")
api.add_resource(Student, "/api/<string:_id>",
                          endpoint="_id")
