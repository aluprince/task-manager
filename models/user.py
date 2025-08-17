from mongoengine import Document, StringField, ListField, IntField

class User(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    phone_number = StringField(required=False)
    password = StringField(required=True)
    meta = {"collection": "Users"} #setting collection name




