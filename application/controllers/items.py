from app import app, db
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from app.models.item import Item

item_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'donor': fields.String,
    'status': fields.String,
    'category': fields.String,
    'charity': fields.String,
    'image': fields.String
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
    help='name parameter is required'
)
item_post_parser.add_argument(
    'description',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
item_post_parser.add_argument(
    'price',
    type=float,
    required=True,
    location=['json'],
    help='name parameter is required'
)
item_post_parser.add_argument(
    'donor',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
item_post_parser.add_argument(
    'status',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
item_post_parser.add_argument(
    'category',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
item_post_parser.add_argument(
    'charity',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
item_post_parser.add_argument(
    'image',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)

class ItemResources(Resource):
    def get(self, item_id=None):
        if item_id:
            item = Item.query.filter_by(id=item_id).first()
            return marshal(item, item_fields)
        else:
            items = Item.query.all()
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

        if 'title' in request.json:
            item.title = request.json['title']
        if 'description' in request.json:
            item.description = request.json['description']
        if 'price' in request.json:
            item.price = request.json['price']
        if 'donor' in request.json:
            item.donor = request.json['donor']
        if 'status' in request.json:
            item.status = request.json['status']
        if 'category' in request.json:
            item.category = request.json['category']
        if 'charity' in request.json:
            item.charity = request.json['charity']
        if 'image' in request.json:
            item.image = request.json['image']

        db.session.commit()
        return item

    @marshal_with(item_fields)
    def delete(self, item_id=None):
        item = Item.query.get(item_id)

        db.session.delete(item)
        db.session.commit()

        return item
