from datetime import datetime, timedelta
from math import trunc
from application import db, app_config
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
import jwt
import os


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    admin = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.BigInteger())

    bids = db.relationship('Bid', backref='users', lazy='select')
    items = db.relationship('Item', backref='users', lazy='select')

    def hash_password(self, act_password):
        self.password = pwd_context.encrypt(act_password)

    def verify_password(self, act_password):
        return pwd_context.verify(act_password, self.password)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('TOKEN_SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, os.getenv('TOKEN_SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<id {}>'.format(self.id)
