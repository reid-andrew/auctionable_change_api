from datetime import datetime, timedelta
from math import trunc
from application import db, app_config
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
import jwt
import os


class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    blacklisted_on = db.Column(db.DateTime)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
