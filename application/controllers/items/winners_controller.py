from application import db
from application.models.user import User
from application.models.item import Item
from application.models.bid import Bid
from flask import request, abort
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from datetime import datetime
from math import trunc

item_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'status': fields.String,
    'category': fields.String,
    'charity': fields.String,
    'charity_url': fields.String,
    'charity_score': fields.Integer,
    'charity_score_image': fields.String,
    'image': fields.String,
    'auction_length': fields.Integer,
    'created_at': fields.String,
    'auction_end': fields.String,
    'bids': fields.List(
        fields.Nested(
            {
                'id': fields.Integer,
                'item_id': fields.Integer,
                'amount': fields.Float,
                'winner': fields.Boolean,
                'created_at': fields.String,
            }
        )
    )
}

item_list_fields = {
    'count': fields.Integer,
    'items': fields.List(fields.Nested(item_fields))
}

item_post_parser = reqparse.RequestParser()
item_post_parser.add_argument(
    'user_id',
    type=int,
    required=True,
    location=['json'],
    help='user_id parameter is required'
)
item_post_parser.add_argument(
    'title',
    type=str,
    required=True,
    location=['json'],
    help='title parameter is required'
)
item_post_parser.add_argument(
    'description',
    type=str,
    required=True,
    location=['json'],
    help='description parameter is required'
)
item_post_parser.add_argument(
    'price',
    type=float,
    required=True,
    location=['json'],
    help='price parameter is required'
)
item_post_parser.add_argument(
    'status',
    type=str,
    required=False,
    location=['json']
)
item_post_parser.add_argument(
    'category',
    type=str,
    required=True,
    location=['json'],
    help='category parameter is required'
)
item_post_parser.add_argument(
    'charity',
    type=str,
    required=True,
    location=['json'],
    help='charity parameter is required'
)
item_post_parser.add_argument(
    'charity_url',
    type=str,
    required=True,
    location=['json'],
    help='charity_url parameter is required'
)
item_post_parser.add_argument(
    'charity_score',
    type=int,
    required=True,
    location=['json'],
    help='charity_score parameter is required'
)
item_post_parser.add_argument(
    'charity_score_image',
    type=str,
    required=True,
    location=['json'],
    help='charity_score_image parameter is required'
)
item_post_parser.add_argument(
    'image',
    type=str,
    required=True,
    location=['json'],
    help='image parameter is required'
)
item_post_parser.add_argument(
    'auction_length',
    type=int,
    required=False,
    location=['json']
)
item_post_parser.add_argument(
    'created_at',
    type=datetime,
    required=False,
    location=['json']
)
item_post_parser.add_argument(
    'auction_end',
    type=datetime,
    required=True,
    location=['json']
)

class WinnerResources(Resource):
    def post(self):
        current_time = trunc(datetime.now().timestamp())
        available_items = Item.query.filter(Item.status=='available',
                                            Item.auction_end<=current_time,
                                            Item.bids!=None).all()
        if not available_items:
            abort(404, description='No pending winners')
        else:
            for item in available_items:
                high_bid = 0.0
                pending_winner = None
                submitted_bids = Bid.query.filter_by(item_id=item.id).order_by(Bid.created_at).all()
                for bid in submitted_bids:
                    if bid.amount > item.price and bid.amount > high_bid:
                        high_bid = bid.amount
                        pending_winner = bid.id
                    else:
                        high_bid = high_bid

                winner = Bid.query.filter_by(id=pending_winner).first()
                if winner:
                    item.status='pending'
                    db.session.add(item)

                    winner.winner = True
                    db.session.add(winner)
                    db.session.commit()
                else:
                    item.status='available'
                    seconds = item.auction_length * 60
                    item.auction_end = current_time + seconds
                    db.session.add(item)
                    db.session.commit()

        pending_items = Item.query.filter_by(status='pending').all()
        if not pending_items:
            abort(404, description='No pending winners')
        else:
            return marshal({
                'count': len(pending_items),
                'items': [marshal(i, item_fields) for i in pending_items]
            }, item_list_fields)
