from pymodm import MongoModel, EmbeddedMongoModel, fields, connect


connect('mongodb://localhost:27017/app')


class User(MongoModel):
    email = fields.EmailField(primary_key=True, required=True)
    handle = fields.CharField(required=True)
    password = fields.CharField(required=True)

    class Meta:
        collection_name = "users"

class Entry(MongoModel):
    date = fields.DateTimeField(required=True)
    pain_level_morning = fields.IntegerField(required=True)
    pain_level_prev_day = fields.IntegerField(required=True)
    sedentary_prev_day = fields.BooleanField(required=True)
    notes_on_prev_day = fields.CharField(required=True)
    author = fields.ReferenceField(User, required=True)

    class Meta:
        collection_name = "entries"
