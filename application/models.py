from flask import jsonify
from application import mongo
from bson.objectid import ObjectId
from datetime import datetime
import decimal


class Student(mongo.Document):
    firstname = mongo.StringField(max_length=255, required=True)
    lastname = mongo.StringField(max_length=255, required=True)
    sex = mongo.StringField(required=True, choices=(("Male", "M"),
        ("Female", "F"), ("Other", "O")))
    birthday = mongo.DateTimeField(required=True)
    email = mongo.EmailField(max_length=255, required=True)
    socialmedia = mongo.ListField(field=mongo.StringField(max_length=255))


class AttractionDetails(mongo.EmbeddedDocument):
    elevation = mongo.StringField(max_length=255)
    fee = mongo.DecimalField(min_value=0, max_value=10000,
        precision=2, rounding=decimal.ROUND_DOWN)
    size = mongo.StringField(max_length=255)
    catagory = mongo.StringField(max_length=255)


class Attraction(mongo.DynamicDocument):
    name = mongo.StringField(max_length=255, required=True)
    description = mongo.StringField(max_length=65535, required=True)
    details = mongo.EmbeddedDocumentField(document_type=AttractionDetails)
    location = mongo.PointField()

    meta = {'allow_inheritance': True}

class MajorAttraction(Attraction):
    pass


class MinorAttraction(Attraction):
    majorAttraction = mongo.ReferenceField(document_type=MajorAttraction,
        required=True)
    reviews = mongo.IntField(required=True, default=0)


class User(mongo.DynamicDocument):
    firstname = mongo.StringField(max_length=255, required=True)
    lastname = mongo.StringField(max_length=255, required=True)
    username = mongo.StringField(max_length=255, required=True)
    password = mongo.StringField(max_length=255, required=True)
    timestamp = mongo.DateTimeField(required=True, default=datetime.utcnow())
    admin = mongo.BooleanField(required=True, default=False)
    email = mongo.EmailField(max_length=255, required=True)


class Review(mongo.DynamicDocument):
    user = mongo.ReferenceField(document_type=User, required=True)
    body = mongo.StringField(max_length=65535, required=True)
    timestamp = mongo.DateTimeField(required=True, default=datetime.utcnow())
    attraction = mongo.ReferenceField(document_type=Attraction,
        required = True)
    upvotes = mongo.IntField(required=True, default=0)

    def increment_upvotes(self):
        self.upvotes += 1


#TODO: Add view all reviews for majorAttractions and minorAttractions
#TODO: Add upvote functionality to reviews
#TODO: Expand users and attractions in history and reviews and check other places
#TODO: Add urls to resourses
