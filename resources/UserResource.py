import falcon
from  bson import json_util
import re
from models.UserModel import UserModel
import UserWrite

class UserGetResource:
    def __init__(self,db):
        self.collection = db['users']

    def on_get(self,req,resp,email):
        user=self.collection.find_one( {"email":email}, {'_id': 0} ) #Find by email

        if user: # if the user is found
            resp.status = falcon.HTTP_200
            resp.media=user

        else: # user not found
            resp.status=falcon.HTTP_404
            resp.media={'message':'User not found'}


class UserPostResource:
    def __init__(self,db):
        self.collection = db['users']

    def on_post(self,req,resp):
        data=req.media


        if not data.get('name') or not data.get('email') or not data.get('age'):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'User name, age and email are required fields'}
            return

        if not isinstance(data.get('age'), int) or data.get('age') < 0:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid age'}
            return

        if self.collection.find_one({"email": data.get('email')}):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Email already exists'}
            return

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data.get('email')):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid email address'}
            return

        user = UserModel.from_dict(data)
        self.collection.insert_one(user.to_dict())
        UserWrite.write_user_to_file(user.to_dict())
        resp.status = falcon.HTTP_201
        resp.media = {'message': 'User created successfully'}