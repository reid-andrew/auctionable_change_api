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
            return marshal(item, item_list_fields)
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
