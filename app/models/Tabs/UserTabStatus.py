import enum
from datetime import datetime

from app import db


class UserTabStatus(enum.Enum):
    PENDING = 1
    APPROVED = 2
    DECLINED = 3
    CLOSED = 4


class UserTabStatus(db.Model):
    """
        Model for status of users in a tab
    """
    __tablename__ = 'user_tab_status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tab = db.Column(db.Integer, db.ForeignKey('tabs.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    balance = db.Column(db.NUMERIC, nullable=False, default=0)
    status = db.Column(db.Enum(UserTabStatus), nullable=False, unique=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                                   onupdate=datetime.utcnow)

