import falcon
from bson import json_util
from pymongo import MongoClient

class UserModel:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
        )
