from math import trunc
from application import db
from flask import request, abort
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from application.models.bid import Bid
from application.models.item import Item
from application.models.user import User
from datetime import datetime

bid_fields = {
    'id': fields.Integer,
    'item_id': fields.Integer,
    'user_id': fields.Integer,
    'amount': fields.Float,
    'winner': fields.Boolean,
    'created_at': fields.Integer,
}

bid_list_fields = {
    'count': fields.Integer,
    'bids': fields.List(fields.Nested(bid_fields))
}

bid_post_parser = reqparse.RequestParser()
bid_post_parser.add_argument(
    'item_id',
    type=int,
    required=True,
    location=['json'],
    help='item_id parameter is required'
)
bid_post_parser.add_argument(
    'user_id',
    type=int,
    required=True,
    location=['json'],
    help='user_id parameter is required'
)
bid_post_parser.add_argument(
    'amount',
    type=float,
    required=True,
    location=['json'],
    help='amount parameter is required'
)
bid_post_parser.add_argument(
    'winner',
    type=bool,
    required=False,
    location=['json']
)
bid_post_parser.add_argument(
    'created_at',
    type=int,
    required=False,
    location=['json']
)

class WinnerBidResources(Resource):
    def get(self, bid_id=None):
        bids = Bid.query.filter_by(winner=True).all()
        return marshal({
            'count': len(bids),
            'bids': [marshal(i, bid_fields) for i in bids]
        }, bid_list_fields)
