from flask import jsonify
from application import mongo
from bson.objectid import ObjectId

class Student(mongo.Document):
    firstname = mongo.StringField(max_length=255, required=True)
    lastname = mongo.StringField(max_length=255, required=True)
    sex = mongo.StringField(required=True, choices=(("Male", "M"),
        ("Female", "F"), ("Other", "O")))
    birthday = mongo.DateTimeField(required=True)
    email = mongo.EmailField(max_length=255, required=True)
    socialmedia = mongo.ListField(mongo.StringField(max_length=255))


class MajorAttraction(mongo.DynamicDocument):
    name = mongo.StringField(max_length=255, required=True)
    description = mongo.StringField(max_length=65535, required=True)
    details = mongo.DictField()
    location = mongo.PointField()


class MinorAttraction(mongo.DynamicDocument):
    name = mongo.StringField(max_length=255, required=True)
    description = mongo.StringField(max_length=65535, required=True)
    majorAttraction = mongo.ReferenceField(document_type=MajorAttraction,
        required=True)
    details = mongo.DictField()
    location = mongo.PointField()
