from flask import jsonify
from application import mongo
from bson.objectid import ObjectId


class StudentModel():
    def getData(self, _id=None):
        if _id:
            data = mongo.db.student.find_one(
                {'_id': ObjectId(_id)})
            data['_id'] = str(data['_id'])
            return data
        else:
            data = []
            cursor = mongo.db.student.find()
            for student in cursor:
                student['_id'] = str(student['_id'])
                data.append(student)
            return data
