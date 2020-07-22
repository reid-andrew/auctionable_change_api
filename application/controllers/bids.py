from application import db
from flask import request
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from application.models.bid import Bid

bid_fields = {
    'id': fields.Integer,
    'bidder_name': fields.String,
    'bidder_email': fields.String,
    'amount': fields.Float,
    'stress_address': fields.String,
    'city': fields.String,
    'state': fields.String,
    'zip_code': fields.String,
    'receipt': fields.String
}

bid_list_fields = {
    'amount': fields.Integer,
    'bids': fields.List(fields.Nested(bid_fields))
}

bid_post_parser = reqparse.RequestParser()
bid_post_parser.add_argument(
    'bidder_name',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
bid_post_parser.add_argument(
    'bidder_email',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
bid_post_parser.add_argument(
    'amount',
    type=float,
    required=True,
    location=['json'],
    help='name parameter is required'
)
bid_post_parser.add_argument(
    'street_address',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
bid_post_parser.add_argument(
    'city',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
bid_post_parser.add_argument(
    'state',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
bid_post_parser.add_argument(
    'zip_code',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
bid_post_parser.add_argument(
    'receipt',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)


class BidResources(Resource):
    def get(self, bid_id=None):
        if bid_id:
            bid = Bid.query.filter_by(id=bid_id).first()
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

        bid = Bid(**args)
        db.session.add(bid)
        db.session.commit()

        return bid

    @marshal_with(bid_fields)
    def put(self, bid_id=None):
        bid = Bid.query.get(bid_id)

        if 'bidder_name' in request.json:
            bid.bidder_name = request.json['bidder_name']
        if 'bidder_email' in request.json:
            bid.bidder_email = request.json['bidder_email']
        if 'amount' in request.json:
            bid.amount = request.json['amount']
        if 'street_address' in request.json:
            bid.street_address = request.json['street_address']
        if 'city' in request.json:
            bid.city = request.json['city']
        if 'state' in request.json:
            bid.state = request.json['state']
        if 'zip_code' in request.json:
            bid.zip_code = request.json['zip_code']
        if 'receipt' in request.json:
            bid.receipt = request.json['receipt']

        db.session.commit()
        return bid

    @marshal_with(bid_fields)
    def delete(self, bid_id=None):
        bid = Bid.query.get(bid_id)

        db.session.delete(bid)
        db.session.commit()

        return bid
