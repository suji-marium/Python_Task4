import falcon
from  bson import json_util
import re
from models.user_model import User
from user_write import write_user_to_file

class UserGet:
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

class UserPost:
    def __init__(self, db):
        self.collection = db['users']

    def on_post(self, req, resp):
        data = req.media

        # Check if all the required attributes are provided
        if not all([data.get('name'), data.get('email'), data.get('age')]):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'User name, age and email are required fields'}
            return

        # Check if name is a string
        if not isinstance(data.get('name'), str):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid name'}
            return

        # Check if age is integer and non-negative
        if not isinstance(data.get('age'), int) or data.get('age') < 0:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid age'}
            return

        # Check if the email already exists
        """
        if self.collection.find_one({"email": data.get('email')}):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Email already exists'}
            return
        """
        # Check if the email already exists
        email_count = self.collection.count_documents({"email": data.get('email')})
        if email_count > 0:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Email already exists'}
            return
        """
        try:
            # Check if the email is valid or not
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data.get('email')):
                resp.status = falcon.HTTP_400
                resp.media = {'message': 'Invalid email address'}
                return
        except TypeError as e:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid input data'}
            return
        """
        email = data.get('email')
        if not isinstance(email, str) or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid email address'}
            return

        user = User.__new__(User)
        user.__dict__.update(data)

        self.collection.insert_one(user.__dict__)
        write_user_to_file(user.__dict__)
        resp.status = falcon.HTTP_201
        resp.media = {'message': 'User created successfully'}
