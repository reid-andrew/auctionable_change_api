from application import db, create_app
from flask import request, abort
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from application.models.item import Item

item_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'donor': fields.String,
    'donor_email': fields.String,
    'status': fields.String,
    'category': fields.String,
    'charity': fields.String,
    'charity_url': fields.String,
    'charity_score': fields.Integer,
    'image': fields.String,
    'bids': fields.List(
        fields.Nested(
            {
                'id': fields.Integer,
                'item_id': fields.Integer,
                'bidder_name': fields.String,
                'bidder_email': fields.String,
                'amount': fields.Float,
                'street_address': fields.String,
                'city': fields.String,
                'state': fields.String,
                'zip_code': fields.String,
                'receipt': fields.String
            }
        )
    ),
}

item_list_fields = {
    'count': fields.Integer,
    'items': fields.List(fields.Nested(item_fields))
}

item_post_parser = reqparse.RequestParser()
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
    'donor',
    type=str,
    required=True,
    location=['json'],
    help='donor parameter is required'
)
item_post_parser.add_argument(
    'donor_email',
    type=str,
    required=True,
    location=['json'],
    help='donor parameter is required'
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
    'image',
    type=str,
    required=True,
    location=['json'],
    help='image parameter is required'
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
            if 'donor' in request.json:
                item.donor = request.json['donor']
            if 'donor_email' in request.json:
                item.donor_email = request.json['donor_email']
            if 'category' in request.json:
                item.category = request.json['category']
            if 'charity' in request.json:
                item.charity = request.json['charity']
            if 'charity_url' in request.json:
                item.charity_url = request.json['charity_url']
            if 'charity_score' in request.json:
                item.charity_score = request.json['charity_score']
            if 'image' in request.json:
                item.image = request.json['image']

            db.session.commit()
            return item

    @marshal_with(item_fields)
    def delete(self, item_id=None):
        item = Item.query.get(item_id)
        if not item:
            abort(404, description='That item does not exist')
        else:
            db.session.delete(item)
            db.session.commit()

            return item
