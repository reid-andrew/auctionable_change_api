from application import db
from flask import request, abort
from flask_restful import Resource, reqparse
from flask_restful import fields, marshal_with, marshal
from application.models.final import Final

final_fields = {
    'id': fields.Integer,
    'street_address': fields.String,
    'city': fields.String,
    'state': fields.String,
    'zip_code': fields.String,
    'receipt': fields.String
}

final_list_fields = {
    'count': fields.Integer,
    'finals': fields.List(fields.Nested(final_fields))
}

final_post_parser = reqparse.RequestParser()
final_post_parser.add_argument(
    'street_address',
    type=str,
    required=True,
    location=['json'],
    help='street_address parameter is required'
)
final_post_parser.add_argument(
    'city',
    type=str,
    required=True,
    location=['json'],
    help='city parameter is required'
)
final_post_parser.add_argument(
    'state',
    type=str,
    required=True,
    location=['json'],
    help='state parameter is required'
)
final_post_parser.add_argument(
    'zip_code',
    type=str,
    required=True,
    location=['json'],
    help='zip_code parameter is required'
)
final_post_parser.add_argument(
    'receipt',
    type=str,
    required=True,
    location=['json'],
    help='receipt parameter is required'
)


class FinalResources(Resource):
    def get(self, final_id=None):
        if final_id:
            final = Final.query.filter_by(id=final_id).first()
            if not final:
                abort(404, description='That final bidder does not exist')
            else:
                return marshal(final, final_fields)
        else:
            finals = Final.query.all()
            return marshal({
                'count': len(finals),
                'finals': [marshal(i, final_fields) for i in finals]
            }, final_list_fields)

    @marshal_with(final_fields)
    def post(self):
        args = final_post_parser.parse_args()
        final = Final(**args)
        db.session.add(final)
        db.session.commit()

        return final

    @marshal_with(final_fields)
    def put(self, final_id=None):
        final = Final.query.get(final_id)
        if not final:
            abort(404, description='That final bidder does not exist')
        else:
            if 'street_address' in request.json:
                final.street_address = request.json['street_address']
            if 'city' in request.json:
                final.city = request.json['city']
            if 'state' in request.json:
                final.state = request.json['state']
            if 'zip_code' in request.json:
                final.zip_code = request.json['zip_code']
            if 'receipt' in request.json:
                final.receipt = request.json['receipt']

            db.session.commit()
            return final

    @marshal_with(final_fields)
    def delete(self, final_id=None):
        final = Final.query.get(final_id)
        if not final:
            abort(404, description='That final bidder does not exist')
        else:
            db.session.delete(final)
            db.session.commit()

            return final
