from datetime import datetime, timedelta
from application import db


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Float())
    status = db.Column(db.String(), default='available')
    category = db.Column(db.String())
    charity = db.Column(db.String())
    charity_url = db.Column(db.String())
    charity_score = db.Column(db.Integer())
    image = db.Column(db.String())
    auction_length = db.Column(db.Integer(), default=timedelta(minutes=5))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    auction_end = db.Column(db.DateTime(), default=created_at + auction_length)

    bids = db.relationship('Bid', backref='items', lazy='select')

    def __repr__(self):
        return '<id {}>'.format(self.id)
