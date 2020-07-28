from application import db


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Float())
    donor = db.Column(db.String())
    donor_email = db.Column(db.String())
    status = db.Column(db.String(),default='available')
    category = db.Column(db.String())
    charity = db.Column(db.String())
    charity_url = db.Column(db.String())
    charity_score = db.Column(db.Integer())
    charity_score_image = db.Column(db.String())
    image = db.Column(db.String())

    bids = db.relationship('Bid', backref='items', lazy='select')

    def __repr__(self):
        return '<id {}>'.format(self.id)
