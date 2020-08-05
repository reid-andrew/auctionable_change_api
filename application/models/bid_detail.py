from application import db
from datetime import datetime


class BidDetail(db.Model):
    __tablename__ = 'bid_details'

    id = db.Column(db.Integer, primary_key=True)
    bid_id = db.Column(db.Integer, db.ForeignKey('bids.id'), nullable=False)
    street_address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    zip_code = db.Column(db.String())
    receipt = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return '<id {}>'.format(self.id)
