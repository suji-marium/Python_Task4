from http.client import responses

import falcon
import pytest
from falcon.testing import TestClient
from unittest.mock import MagicMock
from routes.api import create_routes


@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture()
def app(mock_db):
    return create_routes(mock_db)

@pytest.fixture
def client(app):
    return TestClient(app)


def test_user_post_success(client, mock_db):
    mock_db['users'].count_documents.return_value = 0
    response = client.simulate_post('/user-post', json={'name': 'John Doe', 'age': 30, 'email': 'john@example.com'})

    assert response.status == falcon.HTTP_201
    assert response.json == {'message': 'User created successfully'}

def test_user_post_missing_fields(client,mock_db):
    response = client.simulate_post('/user-post',json={'age':12, 'email':'ramu@1234'})

    assert response.status == falcon.HTTP_400
    assert response.json == {'message': 'User name, age and email are required fields'}

def test_user_post_invalid_name(client,mock_db):
    response = client.simulate_post('/user-post',json={'name': 8, 'age': 12, 'email': 'john@example.com'})
    assert response.status == falcon.HTTP_400
    assert response.json == {'message': 'Invalid name'}

def test_user_post_invalid_age(client,mock_db):
    response = client.simulate_post('/user-post',json={'name': 'John Doe', 'age': -9, 'email': 'john@example.com'})
    assert response.status == falcon.HTTP_400
    assert response.json == {'message': 'Invalid age'}

def test_user_post_invalid_email(client, mock_db):
    mock_db['users'].count_documents.return_value = 0
    response = client.simulate_post('/user-post', json={'name': 'Jane Doe', 'age': 30, 'email': 'janeinvalid'})

    assert response.status == falcon.HTTP_400
    assert response.json == {'message': 'Invalid email address'}


def test_user_post_duplicate_email(client, mock_db):
    mock_db['users'].count_documents.return_value = 1
    response = client.simulate_post('/user-post', json={'name': 'John Doe', 'age': 30, 'email': 'john@example.com'})

    assert response.status == falcon.HTTP_400
    assert response.json == {'message': 'Email already exists'}



def test_user_get_success(client, mock_db):
    mock_db['users'].find_one.return_value = {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}
    response = client.simulate_get('/user-get/john@example.com')

    assert  response.status == falcon.HTTP_200
    assert  response.json == {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}

def test_user_get_not_found(client, mock_db):
    mock_db['users'].find_one.return_value = None
    response = client.simulate_get('/user-get/rani@example.com')

    assert  response.status == falcon.HTTP_404
    assert  response.json == {'message':'User not found'}

def test_user_get_all_success(client, mock_db):
   mock_db['users'].find.return_value = [
       {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'},
       {'name': 'Kumar L', 'age': 35, 'email': 'kumar@example.com'}
   ]

   response = client.simulate_get('/user-get')
   assert response.status == falcon.HTTP_200
   assert  response.json == [
       {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'},
       {'name': 'Kumar L', 'age': 35, 'email': 'kumar@example.com'}
   ]


