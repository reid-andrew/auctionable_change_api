from application import db


class Final(db.Model):
    __tablename__ = 'finals'

    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    zip_code = db.Column(db.String())
    receipt = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id)
