from pymodm import MongoModel, EmbeddedMongoModel, fields, connect
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

connect('mongodb://localhost:27017/app')
ph = PasswordHasher()

class User(MongoModel):
    email = fields.EmailField(primary_key=True, required=True)
    hashed_password = fields.CharField(required=True)

    class Meta:
        collection_name = "users"

    def hash_password(self) -> None:
        self.hashed_password = ph.hash(self.hashed_password)

    def check_password(self, password: str) -> bool:
        try:
            ph.verify(self.hashed_password, password)
            return True
        except VerifyMismatchError:
            return False


class Entry(MongoModel):
    date = fields.DateTimeField(required=True)
    pain_level_morning = fields.IntegerField(required=True)
    pain_level_prev_day = fields.IntegerField(required=True)
    sedentary_prev_day = fields.BooleanField(required=True)
    notes_on_prev_day = fields.CharField(required=True)
    author = fields.ReferenceField(User, required=True)

    class Meta:
        collection_name = "entries"
