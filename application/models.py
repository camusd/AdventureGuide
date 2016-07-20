from flask import jsonify
from application import mongo
from bson.objectid import ObjectId

class Student(mongo.Document):
    firstname = mongo.StringField(max_length=255, required=True)
    lastname = mongo.StringField(max_length=255, required=True)
    sex = mongo.StringField(required=True, choices=(("M", "Male"),
        ("F", "Female"), ("O", "Other")))
    birthday = mongo.DateTimeField(required=True)
    email = mongo.EmailField(max_length=255, required=True)
    socialmedia = mongo.ListField(mongo.StringField(max_length=255), required=True)
