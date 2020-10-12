from flask import Flask, Response, request
from pain_tracker.models import User, Entry
from bson import json_util
import json
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

jwt = JWTManager(app)

@app.route("/entry", methods=["POST"])
def post_entry():
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



if __name__ == "__main__":
    app.run()
