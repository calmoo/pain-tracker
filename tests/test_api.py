"""
Tests for Flask pain_tracker API
"""

from flask.testing import FlaskClient
from datetime import datetime



class TestCreate:
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
