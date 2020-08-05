from application import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())

    bids = db.relationship('Bid', backref='users', lazy='select')
    items = db.relationship('Item', backref='users', lazy='select')

    def __repr__(self):
        return '<id {}>'.format(self.id)
