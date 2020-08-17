from application import db


class Bid(db.Model):
    __tablename__ = 'bids'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float())
    winner = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.BigInteger())

    bid_detail = db.relationship("BidDetail", uselist=False, backref="bids")

    def __repr__(self):
        return '<id {}>'.format(self.id)
