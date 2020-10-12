"""
Fixtures for tests.
"""
import pytest
from pain_tracker.app import app as flask_app
from flask.testing import FlaskClient
from pymongo import MongoClient



@pytest.fixture
def client() -> FlaskClient:
    """
    A Flask test client.
    """
    client = MongoClient('mongodb://localhost:27017')
    client.drop_database('entries')
    client.close()
    mytestclient = flask_app.test_client()
    return mytestclient
