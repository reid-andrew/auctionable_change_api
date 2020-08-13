from datetime import datetime, timedelta
from application import db


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    expiry = db.Column(db.DateTime)

    def check_token(self, auth_token):
        token = Token.query.filter_by(token=str(auth_token)).first()
        if token:
            current_time = datetime.now()
            if token.expiry - current_time > timedelta(days=1):
                return True
        else:
            return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
