from flask import Flask, Response, request
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError
from pain_tracker.models import User, Entry
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
import json
import os
import datetime


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

jwt = JWTManager(app)

@app.route("/entry", methods=["POST"])
def post_entry() -> Response:
    payload = request.json
    entry = Entry(date=payload['date'],
                  pain_level_morning=payload['pain_level_morning'],
                  pain_level_prev_day=payload['pain_level_prev_day'],
                  sedentary_prev_day=payload['sedentary_prev_day'],
                  notes_on_prev_day=payload['notes_on_prev_day'],
                  author=payload['author']
                  )
    entry.save()

    return Response(
        response=json.dumps(payload),
        mimetype="application/json",
        status=201,
    )

@app.route("/signup", methods=["POST"])
def user_signup() -> Response:
    """
    Create user from credentials
    """
    payload = request.json
    user = User(email=payload["email"], hashed_password=payload["password"])
    try:
        user.hash_password()
        user.save(force_insert=True)
        return Response(status=201)
    except ValidationError:
        return Response(
            response=json.dumps({"Error": "Must include email and password"}),
            mimetype="application/json",
            status=400
        )
    except DuplicateKeyError:
        return Response(
            response=json.dumps({"Error": "Email already exists"}), status=409
        )



@app.route("/login", methods=["POST"])
def user_login() -> Response:
    """
    Login user with credentials
    """
    payload = request.json
    email, password = payload['email'], payload['password']
    user = User.objects.get({'_id': email})
    if user.check_password(password=password):
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=user.email,expires_delta=expires)
        return Response(
            response=json.dumps({"token": access_token}),
            mimetype="application/json",
            status=200,
    )
    else:
        return Response(
            response=json.dumps({"Error": "Password incorrect"}), status=401
        )



if __name__ == "__main__":
    app.run()
