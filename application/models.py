from flask import jsonify
from application import mongo
from bson.objectid import ObjectId


class StudentModel():
    def getData(self, object_id=None):
        if object_id:
            survey_data = mongo.db.student.find_one(
                {'_id': ObjectId(object_id)})
            survey_data['_id'] = str(survey_data['_id'])
            return survey_data
        else:
            data = []
            cursor = mongo.db.student.find()
            for student in cursor:
                student['_id'] = str(student['_id'])
                data.append(student)
            return data
