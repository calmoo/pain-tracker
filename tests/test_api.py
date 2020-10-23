"""
Tests for Flask pain_tracker API
"""

from flask.testing import FlaskClient
from datetime import datetime
from typing import List
from bson.json_util import dumps



class TestCreateEntry:
    def test_create(self, client: FlaskClient, jwt_token: str) -> None:
        """"""
        new_entry = {
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
            "pain_level_morning": 1,
            "pain_level_prev_day": 2,
            "sedentary_prev_day": True,
            "notes_on_prev_day": "Not enough walking",
        }
        post_res = client.post("/entry", json=new_entry, headers={"Authorization": jwt_token})
        assert post_res.get_json() == new_entry
        assert post_res.status_code == 201

class TestGetAllEntries:

    def test_get_all(self, client: FlaskClient, jwt_token: str) -> None:
        """
        It is possible to retrieve all Entry items created by the user
        """
        new_entry = {
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
            "pain_level_morning": 1,
            "pain_level_prev_day": 2,
            "sedentary_prev_day": True,
            "notes_on_prev_day": "Not enough walking",
        }

        new_entry_2 = {
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
            "pain_level_morning": 2,
            "pain_level_prev_day": 2,
            "sedentary_prev_day": True,
            "notes_on_prev_day": "Not enough walking",
        }
        first_post = client.post(
            "/entry",
            json=new_entry,
            headers={"Authorization": jwt_token},
        )
        second_post = client.post(
            "/entry",
            json=new_entry_2,
            headers={"Authorization": jwt_token},
        )

        res = client.get("/entry", headers={"Authorization": jwt_token})
        get_data = res.get_json()
        expected_data = [new_entry,new_entry_2]
        assert get_data == expected_data


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