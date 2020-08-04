from application import db
from flask import request, abort
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from application.models.bid import Bid
from application.models.item import Item

bid_fields = {
    'id': fields.Integer,
    'item_id': fields.Integer,
    'bidder_name': fields.String,
    'bidder_email': fields.String,
    'amount': fields.Float
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
    'bidder_name',
    type=str,
    required=True,
    location=['json'],
    help='bidder_name parameter is required'
)
bid_post_parser.add_argument(
    'bidder_email',
    type=str,
    required=True,
    location=['json'],
    help='bidder_email parameter is required'
)
bid_post_parser.add_argument(
    'amount',
    type=float,
    required=True,
    location=['json'],
    help='amount parameter is required'
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
        if not item:
            abort(404, description='That item does not exist')
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
            if 'bidder_name' in request.json:
                bid.bidder_name = request.json['bidder_name']
            if 'bidder_email' in request.json:
                bid.bidder_email = request.json['bidder_email']
            if 'amount' in request.json:
                bid.amount = request.json['amount']

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
