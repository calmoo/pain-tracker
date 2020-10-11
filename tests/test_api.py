"""
Tests for Flask pain_tracker API
"""

from flask.testing import FlaskClient


class TestCreate:
    def test_create(self, client: FlaskClient) -> None:
        """"""
        new_entry = {
            "pain_level_morning": 1,
            "pain_level_prev_day": 2,
            "sedentary_previous_day": True,
            "notes_on_previous_day": "Not enough walking",
        }
        post_res = client.post("/entry", json=new_entry)
        assert post_res.data == 201
