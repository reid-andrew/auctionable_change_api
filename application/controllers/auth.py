from flask_restful import Resource, reqparse
from flask_restful import fields, marshal
from application.models.user import User
from flask_login import current_user, login_user
from flask import abort, make_response, jsonify, request

auth_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password': fields.String
}

auth_list_fields = {
    'count': fields.Integer,
    'auth': fields.List(fields.Nested(auth_fields))
}

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument(
    'id',
    type=str,
    required=False,
    location=['json']
)
user_post_parser.add_argument(
    'email',
    type=str,
    required=False,
    location=['json']
)
user_post_parser.add_argument(
    'password',
    type=str,
    required=False,
    location=['json']
)


class LoginResources(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        if current_user.is_authenticated:
            abort(400, description='User already logged in')
        user = User.query.filter_by(email=email).first()
        if user is None or not user.verify_password(password):
            abort(400, description='Username or password incorrect')
        user = User.query.filter_by(email=email).first()
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'message': 'Successfully logged in.',
            'user_id': user.id,
            'user_token': auth_token.decode()
        }
        return make_response(jsonify(response_object), 200)


class LogoutResources(Resource):
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(response_object)), 200
                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object)), 403

