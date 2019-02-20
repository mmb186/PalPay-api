from app import db
import enum
from datetime import datetime

from app.models.Tabs.enums import UserTabStatus, TabTransactionStatus


class TransactionType(enum.Enum):
    WITHDRAW = 'withdraw'
    DEPOSIT = 'deposit'


class TabTransaction(db.Model):
    """
        Model to represent A tab Transaction
    """
    __tablename__ = 'tab_transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tab_id = db.Column(db.Integer, db.ForeignKey('tabs.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False, unique=False)
    status = db.Column(db.Enum(TabTransactionStatus), nullable=False, default=TabTransactionStatus.PENDING)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                                   onupdate=datetime.utcnow)

    def __init__(self, tab_id, creator_id, transaction_type):
        self.tab_id = tab_id
        self.created_by_id = creator_id
        self.transaction_type = transaction_type

    def save(self):
        db.sessiong.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_by_id(cls, tab_transaction_id):
        return cls.query.filter_by(id=tab_transaction_id).first()

