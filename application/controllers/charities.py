from flask import request
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from application.popos.charity import charitites

charity_fields = {
    'id': fields.Integer,
    'url': fields.String,
    'name': fields.String,
    'rating': fields.Integer
}

charity_list_fields = {
    'count': fields.Integer,
    'charities': fields.List(fields.Nested(charity_fields))
}

item_post_parser = reqparse.RequestParser()
item_post_parser.add_argument(
    'id',
    type=str,
    required=False,
    location=['json']
)
item_post_parser.add_argument(
    'url',
    type=str,
    required=False,
    location=['json']
)
item_post_parser.add_argument(
    'name',
    type=str,
    required=False,
    location=['json']
)
item_post_parser.add_argument(
    'rating',
    type=str,
    required=False,
    location=['json']
)

class CharityResources(Resource):
    def get(self, search_term=None):
        charities = charitites(search_term)

        return marshal({
            'count': len(charities),
            'charities': [marshal(c, charity_fields) for c in charities]
        }, charity_list_fields)
