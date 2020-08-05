from application import db
from flask import request, abort
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from application.models.item import Item
from application.models.user import User
from datetime import datetime

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
                'created_at': fields.DateTime,
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
    required=False,
    location=['json']
)


class ItemResources(Resource):
    def get(self, item_id=None):
        if item_id:
            item = Item.query.filter_by(id=item_id).first()
            if not item:
                abort(404, description='That item does not exist')
            else:
                return marshal(item, item_fields)
        else:
            items = Item.query.filter_by(status='available').all()
            return marshal({
                'count': len(items),
                'items': [marshal(i, item_fields) for i in items]
            }, item_list_fields)

    @marshal_with(item_fields)
    def post(self):
        args = item_post_parser.parse_args()

        user = User.query.filter_by(id=args["user_id"]).first()
        if not user:
            abort(404, description='That user does not exist')
        else:
            item = Item(**args)
            db.session.add(item)
            db.session.commit()

        return item

    @marshal_with(item_fields)
    def put(self, item_id=None):
        item = Item.query.get(item_id)
        if not item:
            abort(404, description='That item does not exist')
        else:
            if 'title' in request.json:
                item.title = request.json['title']
            if 'description' in request.json:
                item.description = request.json['description']
            if 'price' in request.json:
                item.price = request.json['price']
            if 'category' in request.json:
                item.category = request.json['category']
            if 'charity' in request.json:
                item.charity = request.json['charity']
            if 'charity_url' in request.json:
                item.charity_url = request.json['charity_url']
            if 'charity_score' in request.json:
                item.charity_score = request.json['charity_score']
            if 'charity_score_image' in request.json:
                item.charity_score_image = request.json['charity_score_image']
            if 'image' in request.json:
                item.image = request.json['image']
            if 'auction_length' in request.json:
                item.auction_length = request.json['auction_length']
            if 'auction_end' in request.json:
                item.auction_end = request.json['auction_end']
            db.session.commit()
            return item

    @marshal_with(item_fields)
    def delete(self, item_id=None):
        item = Item.query.get(item_id)
        if not item:
            abort(404, description='That item does not exist')
        elif not item.bids == []:
            abort(403, description='Cannot delete item with associated bids')
        else:
            db.session.delete(item)
            db.session.commit()

            return item
