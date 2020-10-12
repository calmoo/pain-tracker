"""
Tests for Flask pain_tracker API
"""

from flask.testing import FlaskClient
from datetime import datetime



class TestCreateEntry:
    def test_create(self, client: FlaskClient) -> None:
        """"""
        new_entry = {
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
            "pain_level_morning": 1,
            "pain_level_prev_day": 2,
            "sedentary_prev_day": True,
            "notes_on_prev_day": "Not enough walking",
            "author":"john"
        }
        post_res = client.post("/entry", json=new_entry)
        assert post_res.get_json() == new_entry
        assert post_res.status_code == 201

class TestUserCreate:
    def test_user_does_not_exist(self, client: FlaskClient) -> None:
        """
        It is possible to create a new user account using an email and password
        """
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        result_from_post = client.post("/signup", json=credentials)
        assert result_from_post.status_code == 201

    def test_user_already_exists(self, client: FlaskClient) -> None:
        """
        A 409 is returned when creating a new user account with an email
        address already in use.
        """
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        result_from_post = client.post("/signup", json=credentials)
        assert result_from_post.status_code == 201
        result_from_second_post = client.post("/signup", json=credentials)
        assert result_from_second_post.status_code == 409

class TestUserLogin:
    def test_user_login_success(self, client: FlaskClient) -> None:
        """
        It is possible to login with a user that has signed up, a JWT token is
        returned.
        """
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        result_from_signup = client.post("/signup", json=credentials)
        assert result_from_signup.status_code == 201
        result_from_login = client.post("/login", json=credentials)
        assert result_from_login.status_code == 200

    def test_user_login_wrong_credentials(self, client: FlaskClient) -> None:
        """
        A 401 is returned when logging in with the wrong password.
        """
        credentials = {
            "email": "test@example.com",
            "password": "example_password",
        }
        credentials_wrong_password = {
            "email": "test@example.com",
            "password": "example_password_1",
        }
        result_from_signup = client.post("/signup", json=credentials)
        assert result_from_signup.status_code == 201
        result_from_login = client.post(
            "/login", json=credentials_wrong_password
        )

        assert result_from_login.status_code == 401