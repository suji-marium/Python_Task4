import falcon
from  bson import json_util
import re
from models.UserModel import UserModel
import UserWrite

class UserGetResource:
    def __init__(self,db):
        self.collection = db['users']

    def on_get(self, req, resp, email=None):
        if email:
            user = self.collection.find_one({"email": email}, {'_id': 0})  # Find by email

            if user:  # if the user is found
                resp.status = falcon.HTTP_200
                resp.media = user

            else:  # user not found
                resp.status = falcon.HTTP_404
                resp.media = {'message': 'User not found'}

        else: # Fetch all users if no email is provided
            users = list(self.collection.find({}, {'_id': 0}))  # Get all users
            resp.status = falcon.HTTP_200
            resp.media = users  # Return list of users

class UserPostResource:
    def __init__(self,db):
        self.collection = db['users']

    def on_post(self,req,resp):
        data=req.media

        # Check if all the required attributes are provided
        if not data.get('name') or not data.get('email') or not data.get('age'):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'User name, age and email are required fields'}
            return

        #  Check if age is integer and non-negative
        if not isinstance(data.get('age'), int) or data.get('age') < 0:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid age'}
            return

        # Check if the email already exist
        if self.collection.find_one({"email": data.get('email')}):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Email already exists'}
            return

        # Check if the email is valid or not
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data.get('email')):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid email address'}
            return

        user = UserModel.from_dict(data)
        self.collection.insert_one(user.to_dict())
        UserWrite.write_user_to_file(user.to_dict())
        resp.status = falcon.HTTP_201
        resp.media = {'message': 'User created successfully'}