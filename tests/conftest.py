"""
Fixtures for tests.
"""
import pytest
import os

from flask.testing import FlaskClient
from pymongo import MongoClient



@pytest.fixture
def client() -> FlaskClient:
    """
    A Flask test client.
    """
    os.environ["JWT_SECRET_KEY"] = "example-secret-key"

    from pain_tracker.app import app as flask_app
    client = MongoClient('mongodb://localhost:27017')
    client.drop_database('app')
    client.close()
    mytestclient = flask_app.test_client()
    return mytestclient

@pytest.fixture
def jwt_token(client: FlaskClient) -> str:
    """
    A JWT token for a new signed up user.
    """

    credentials = {"email": "test@example.com", "password": "example_password"}
    client.post("/signup", json=credentials)
    result_from_login = client.post("/login", json=credentials)
    jwt_token = "Bearer " + str(result_from_login.get_json()["token"])
    return jwt_token