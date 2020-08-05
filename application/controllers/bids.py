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
    'created_at': fields.String
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
    type=datetime,
    required=False,
    location=['json']
)


class BidResources(Resource):
    def get(self, bid_id=None):
        if bid_id:
            bid = Bid.query.filter_by(id=bid_id).first()
            if not bid:
                abort(404, description='That bid does not exist')
            else:
                return marshal(bid, bid_fields)
        else:
            bids = Bid.query.all()
            return marshal({
                'count': len(bids),
                'bids': [marshal(i, bid_fields) for i in bids]
            }, bid_list_fields)

    @marshal_with(bid_fields)
    def post(self):
        args = bid_post_parser.parse_args()

        item = Item.query.filter_by(id=args["item_id"]).first()
        user = User.query.filter_by(id=args["user_id"]).first()

        if not item or user:
            abort(404, description='That item or user does not exist')
        else:
            bid = Bid(**args)
            db.session.add(bid)
            db.session.commit()

            return bid

    @marshal_with(bid_fields)
    def put(self, bid_id=None):
        bid = Bid.query.get(bid_id)
        if not bid:
            abort(404, description='That bid does not exist')
        else:
            if 'amount' in request.json:
                bid.amount = request.json['amount']
            if 'winner' in request.json:
                bid.winner = request.json['winner']

            db.session.commit()
            return bid

    @marshal_with(bid_fields)
    def delete(self, bid_id=None):
        bid = Bid.query.get(bid_id)
        if not bid:
            abort(404, description='That bid does not exist')
        else:
            db.session.delete(bid)
            db.session.commit()

            return bid
