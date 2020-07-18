from app import db

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Float())
    donor = db.Column(db.String())
    status = db.Column(db.String())

    def __init__(self, title, description, price, donor, status):
        self.title = title
        self.description = description
        self.price = price
        self.donor = donor
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'donor': self.donor,
            'status': self.status
        }
