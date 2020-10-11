"""
Fixtures for tests.
"""
import pytest
from pain_tracker.app import app as flask_app

from flask.testing import FlaskClient


@pytest.fixture
def client() -> FlaskClient:
    """
    A Flask test client.
    """
    mytestclient = flask_app.test_client()
    return mytestclient
