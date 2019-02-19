import enum
from datetime import datetime

from app import db


class UserTabStatus(enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    DECLINED = 'declined'


class TabUserStatus(db.Model):
    """
        Model for status and balance of users in a tab
    """
    __tablename__ = 'user_tab_status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tab_id = db.Column(db.Integer, db.ForeignKey('tabs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    balance = db.Column(db.NUMERIC, nullable=False, default=0)
    status = db.Column(db.Enum(UserTabStatus), nullable=False, unique=False,
                       default=UserTabStatus.PENDING)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                                   onupdate=datetime.utcnow)

    def __init__(self, tab_id, user_id):
        self.tab_id = tab_id
        self.user_id = user_id

