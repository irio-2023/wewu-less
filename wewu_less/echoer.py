import flask
from marshmallow import Schema, fields
from marshmallow_dataclass import dataclass

from utils import wewu_cloud_function


@dataclass
class DModel:
    email: str
    title: str
    number: int


class DumbSchema(Schema):
    email = fields.Email()
    title = fields.Str()
    number = fields.Integer()


schema = DumbSchema()


@wewu_cloud_function
def test_handler(request: flask.Request):
    args = request.args.to_dict()
    dumbObject = schema.load(args)
    return str(dumbObject)

@wewu_cloud_function
def second_test_handler(request: flask.Request):
    args = request.args.to_dict()
    return "OKEJ"