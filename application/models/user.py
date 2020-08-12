from datetime import datetime
from application import db
from passlib.apps import custom_app_context as pwd_context
import jwt
import os
from application.models.token import Token


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
                'iat': datetime.utcnow(),
                'sub': int(user_id)
            }
            token = jwt.encode(
                payload,
                os.getenv('TOKEN_SECRET_KEY'),
                algorithm='HS256'
            )

            return token
        except Exception as e:
            return e

    def decode_auth_token(self, auth_token):
        payload = jwt.decode(auth_token, os.getenv('TOKEN_SECRET_KEY'))
        is_token = Token.check_token(self, auth_token=auth_token)
        if not is_token:
            return 'Token expired. Please log in again.'
        else:
            return payload['sub']

    def __repr__(self):
        return '<id {}>'.format(self.id)
