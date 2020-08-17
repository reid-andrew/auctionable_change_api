from math import trunc
from application import db
from flask import request, abort
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from application.models.bid_detail import BidDetail
from application.models.bid import Bid
from application.models.item import Item
from datetime import datetime

bid_detail_fields = {
    'id': fields.Integer,
    'bid_id': fields.Integer,
    'street_address': fields.String,
    'city': fields.String,
    'state': fields.String,
    'zip_code': fields.String,
    'receipt': fields.String,
    'created_at': fields.Integer
}

bid_detail_list_fields = {
    'count': fields.Integer,
    'bid_details': fields.List(fields.Nested(bid_detail_fields))
}

bid_detail_post_parser = reqparse.RequestParser()
bid_detail_post_parser.add_argument(
    'bid_id',
    type=int,
    required=True,
    location=['json'],
    help='bid_id parameter is required'
)
bid_detail_post_parser.add_argument(
    'street_address',
    type=str,
    required=True,
    location=['json'],
    help='street_address parameter is required'
)
bid_detail_post_parser.add_argument(
    'city',
    type=str,
    required=True,
    location=['json'],
    help='city parameter is required'
)
bid_detail_post_parser.add_argument(
    'state',
    type=str,
    required=True,
    location=['json'],
    help='state parameter is required'
)
bid_detail_post_parser.add_argument(
    'zip_code',
    type=str,
    required=True,
    location=['json'],
    help='zip_code parameter is required'
)
bid_detail_post_parser.add_argument(
    'receipt',
    type=str,
    required=True,
    location=['json'],
    help='receipt parameter is required'
)
bid_detail_post_parser.add_argument(
    'created_at',
    type=int,
    required=False,
    location=['json']
)


class BidDetailResources(Resource):
    def get(self, bid_detail_id=None):
        if bid_detail_id:
            bid_detail = BidDetail.query.filter_by(id=bid_detail_id).first()
            if not bid_detail:
                abort(404, description='That bid detail does not exist')
            else:
                return marshal(bid_detail, bid_detail_fields)
        else:
            bid_details = BidDetail.query.all()
            return marshal({
                'count': len(bid_details),
                'bid_details': [marshal(i, bid_detail_fields) for i in bid_details]
            }, bid_detail_list_fields)

    @marshal_with(bid_detail_fields)
    def post(self):
        args = bid_detail_post_parser.parse_args()

        bid = Bid.query.filter_by(id=args["bid_id"]).first()
        if not bid:
            abort(404, description='That bid does not exist')
        else:
            bid_detail = BidDetail(**args)
            dt = trunc(datetime.now().timestamp())
            bid_detail.created_at = dt
            db.session.add(bid_detail)

            item = Item.query.filter_by(id=bid.item_id).first()
            if not item:
                abort(404, description='That item does not exist')
            else:
                item.status='sold'
                db.session.add(item)

            db.session.commit()

            return bid_detail

    @marshal_with(bid_detail_fields)
    def put(self, bid_detail_id=None):
        bid_detail = BidDetail.query.get(bid_detail_id)
        if not bid_detail:
            abort(404, description='That bid detail does not exist')
        else:
            if 'street_address' in request.json:
                bid_detail.street_address = request.json['street_address']
            if 'city' in request.json:
                bid_detail.city = request.json['city']
            if 'state' in request.json:
                bid_detail.state = request.json['state']
            if 'zip_code' in request.json:
                bid_detail.zip_code = request.json['zip_code']
            if 'receipt' in request.json:
                bid_detail.receipt = request.json['receipt']

            db.session.commit()
            return bid_detail

    @marshal_with(bid_detail_fields)
    def delete(self, bid_detail_id=None):
        bid_detail = BidDetail.query.get(bid_detail_id)
        if not bid_detail:
            abort(404, description='That bid detail does not exist')
        else:
            db.session.delete(bid_detail)
            db.session.commit()

            return bid_detail
