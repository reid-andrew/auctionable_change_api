from flask_restful import Resource, reqparse
from flask_restful import fields, marshal
from application.models.item import Item

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
    'created_at': fields.Integer,
    'auction_end': fields.Integer,
    'bids': fields.List(
        fields.Nested(
            {
                'id': fields.Integer,
                'item_id': fields.Integer,
                'amount': fields.Float,
                'winner': fields.Boolean,
                'created_at': fields.Integer,
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
    type=int,
    required=False,
    location=['json']
)
item_post_parser.add_argument(
    'auction_end',
    type=int,
    required=False,
    location=['json']
)


class SoldItemResources(Resource):
    def get(self):
        items = Item.query.filter_by(status='sold').all()
        return marshal({
            'count': len(items),
            'items': [marshal(i, item_fields) for i in items]
        }, item_list_fields)
