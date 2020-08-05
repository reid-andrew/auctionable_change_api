from application import db
from flask import request, abort
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from application.models.user import User
from datetime import datetime

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String,
    'created_at': fields.String,
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
    ),
    'items': fields.List(
        fields.Nested(
            {
                'id': fields.Integer,
                'title': fields.String,
                'description': fields.String,
                'price': fields.Float,
                'status': fields.String,
                'category': fields.String,
                'charity': fields.String,
                'charity_url': fields.String,
                'charity_score': fields.Integer,
                'image': fields.String,
                'auction_length': fields.Integer,
                'created_at': fields.String,
                'auction_end': fields.String
            }
        )
    )
}

user_list_fields = {
    'count': fields.Integer,
    'users': fields.List(fields.Nested(user_fields))
}

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument(
    'first_name',
    type=str,
    required=True,
    location=['json'],
    help='first_name parameter is required'
)
user_post_parser.add_argument(
    'last_name',
    type=str,
    required=True,
    location=['json'],
    help='last_name parameter is required'
)
user_post_parser.add_argument(
    'email',
    type=str,
    required=True,
    location=['json'],
    help='email parameter is required'
)
user_post_parser.add_argument(
    'password',
    type=str,
    required=True,
    location=['json'],
    help='password parameter is required'
)
user_post_parser.add_argument(
    'created_at',
    type=datetime,
    required=False,
    location=['json']
)


class UserResources(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                abort(404, description='That user does not exist')
            else:
                return marshal(user, user_fields)
        else:
            users = User.query.all()
            return marshal({
                'count': len(users),
                'users': [marshal(i, user_fields) for i in users]
            }, user_list_fields)

    @marshal_with(user_fields)
    def post(self):
        args = user_post_parser.parse_args()
        user = User(**args)
        db.session.add(user)
        db.session.commit()

        return user

    @marshal_with(user_fields)
    def put(self, user_id=None):
        user = User.query.get(user_id)
        if not user:
            abort(404, description='That user does not exist')
        else:
            if 'first_name' in request.json:
                user.first_name = request.json['first_name']
            if 'last_name' in request.json:
                user.last_name = request.json['last_name']
            if 'email' in request.json:
                user.email = request.json['email']
            if 'password' in request.json:
                user.password = request.json['password']

            db.session.commit()
            return user

    @marshal_with(user_fields)
    def delete(self, user_id=None):
        user = User.query.get(user_id)
        if not user:
            abort(404, description='That user does not exist')
        else:
            db.session.delete(user)
            db.session.commit()

            return user
