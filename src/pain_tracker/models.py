from pymodm import MongoModel, EmbeddedMongoModel, fields, connect


class User(MongoModel):
    # Make all these fields required, so that if we try to save a User instance
    # that lacks one of these fields, we'll get a ValidationError, which we can
    # catch and render as an error on a form.
    #
    # Use the email as the "primary key" (will be stored as `_id` in MongoDB).
    email = fields.EmailField(primary_key=True, required=True)
    handle = fields.CharField(required=True)
    # `password` here will be stored in plain text! We do this for simplicity of
    # the example, but this is not a good idea in general. A real authentication
    # system should only store hashed passwords, and queries for a matching
    # user/password will need to hash the password portion before of the query.
    password = fields.CharField(required=True)
