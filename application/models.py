from flask import jsonify
from application import mongo, app
from bson.objectid import ObjectId
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
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
    reviews = mongo.IntField(required=True, default=0)
    image = mongo.URLField(max_length=255, required=True)

    def inc_reviews(self):
        self.reviews += 1

    def dec_reviews(self):
        self.reviews -= 1

    meta = {'allow_inheritance': True}

class MajorAttraction(Attraction):
    pass


class MinorAttraction(Attraction):
    majorAttraction = mongo.ReferenceField(document_type=MajorAttraction,
        required=True)


class User(mongo.DynamicDocument):
    firstname = mongo.StringField(max_length=255, required=True)
    lastname = mongo.StringField(max_length=255, required=True)
    username = mongo.StringField(max_length=255, required=True, unique=True)
    password = mongo.StringField(max_length=255, required=True)
    timestamp = mongo.DateTimeField(required=True, default=datetime.utcnow())
    admin = mongo.BooleanField(required=True, default=False)
    email = mongo.EmailField(max_length=255, required=True)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': str(self.id)})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.objects.get_or_404(data['id'])
        return user


class Review(mongo.DynamicDocument):
    user = mongo.ReferenceField(document_type=User, required=True,
        reverse_delete_rule=2)
    body = mongo.StringField(max_length=65535, required=True)
    timestamp = mongo.DateTimeField(required=True, default=datetime.utcnow())
    attraction = mongo.ReferenceField(document_type=Attraction,
        required = True, reverse_delete_rule=2)
    upvotes = mongo.IntField(required=True, default=0)

    def inc_upvotes(self):
        self.upvotes += 1

    def dec_upvotes(self):
        self.upvotes -= 1

#TODO: add rating to attractions
#TODO: sanatize inputs
#TODO: add urls to __init__ arg parser
#TODO: add /api route that returns a bunch of urls
