from datetime import datetime, timedelta
from math import trunc
from application import db, app_config
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
import jwt
import os


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    expiry = db.Column(db.DateTime)

    # def __init__(self, token):
    #     self.token = token
    #     self.expiry = datetime.now()

    def check_blacklist(self, auth_token):
        # check whether auth token has been blacklisted
        res = Token.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
