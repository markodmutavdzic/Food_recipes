from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class UserRegistration(Schema):
    first_name = fields.Str(required=True, validate=Length(max=50))
    last_name = fields.Str(required=True, validate=Length(max=50))
    email = fields.Str(required=True, validate=Length(max=50))
    username = fields.Str(required=True, validate=Length(max=50))
    password = fields.Str(required=True, validate=Length(max=50))


class RecipeCreate(Schema):
    name = fields.Str(required=True, validate=Length(max=50))
    text = fields.Str(required=True)
    ingredients = fields.Str(required=True)


class RecipeRating(Schema):
    recipe_id = fields.Int(required=True)
    rate = fields.Int(required=True, validate=Range(min=1, max=5))


user_register_schema = UserRegistration()
recipe_create_schema = RecipeCreate()
recipe_rate_schema = RecipeRating()
