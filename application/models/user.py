from application import db, app_config
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    created_at = db.Column(db.BigInteger())

    bids = db.relationship('Bid', backref='users', lazy='select')
    items = db.relationship('Item', backref='users', lazy='select')

    def hash_password(self, act_password):
        self.password = pwd_context.encrypt(act_password)

    def verify_password(self, act_password):
        return pwd_context.verify(act_password, self.password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def __repr__(self):
        return '<id {}>'.format(self.id)
