from flask import Flask, Response, request
from pymongo_inmemory import MongoClient
from bson.json_util import dumps
import json
client = MongoClient()
app = Flask(__name__)


@app.route("/entry", methods=["POST"])
def post_entry():
    payload = request.json
    breakpoint()
    db = client['testdb']
    collection = db['test-collection']
    collection.insert_one(payload)
    client.close()
    return Response(
        response=dumps(payload),
        mimetype="application/json",
    )



if __name__ == "__main__":
    app.run()
