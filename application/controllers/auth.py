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


class AuthResources(Resource):
    def post(self):
        # args = user_post_parser.parse_args()
        # auth = User(**args)
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        if current_user.is_authenticated:
            abort(400, description='User already logged in')
        user = User.query.filter_by(email=email).first()
        if user is None or not user.verify_password(password):
            abort(400, description='Username or password incorrect')
        response_object = {
            'status': 'success',
            'message': 'Successfully logged in.'
        }
        return make_response(jsonify(response_object), 200)

    # def get(self, search_term=None):
    #     search_term = "" if search_term is None else search_term
    #     chars = return_charities(search_term)
    #
    #     return marshal({
    #         'count': len(chars),
    #         'charities': [marshal(c, charity_fields) for c in chars]
    #     }, charity_list_fields)
