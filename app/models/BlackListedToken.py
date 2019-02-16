import datetime

from app import db


class BlackListedToken(db.Model):
    """
        Table to store invalid/blacklisted auth tokens
    """
    __tablename__ = 'blacklisted_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    black_list_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.black_list_date = datetime.datetime.utcnow()

    def blacklist(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def is_black_listed(cls, token):
        return cls.query.filter_by(token=token).first() is not None
