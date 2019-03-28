from app import db
from datetime import datetime

from app.models.Tabs.TabTransaction import TabTransaction
from app.models.Tabs.enums import TabTransactionStatus


class UserTabTransactionStatus(db.Model):
    """
        Model to represent the state of the user has with a pending transaction
    """
    __tablename__ = 'user_tab_transaction_status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tab_transaction_id = db.Column(db.Integer, db.ForeignKey('tab_transactions.id'),
                                   nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(TabTransactionStatus), nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                                   onupdate=datetime.utcnow)

    def __init__(self, tab_transaction_id, user_id, status=TabTransactionStatus.PENDING):
        self.tab_transaction_id = tab_transaction_id
        self.user_id = user_id
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_by_tab_transaction_id_and_user_id(cls, tab_transaction_id, user_id):
        return cls.query\
            .filter_by(tab_transaction_id=tab_transaction_id)\
            .filter_by(user_id=user_id)\
            .first()

    @classmethod
    def get_transaction_by_tab_transaction_id(cls, tab_transaction_id):
        return cls.query.filter_by(tab_transaction_id=tab_transaction_id).all()

    @classmethod
    def get_user_transaction_data(cls, user_id, tab_id):
        return db.session\
            .query(TabTransaction, UserTabTransactionStatus)\
            .join(UserTabTransactionStatus)\
            .filter(UserTabTransactionStatus.user_id == user_id)\
            .filter(UserTabTransactionStatus.status != 'DECLINED')\
            .filter(TabTransaction.tab_id == tab_id).all()
