from datetime import datetime

from app import db
import enum


class TabStatus(enum.Enum):
    PENDING = 'pending'
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Tab(db.Model):
    """
        Model for Keeping track of tabs
    """
    __tablename__ = 'tabs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(TabStatus), nullable=False, unique=False, default=TabStatus.PENDING)
    is_group_tab = db.Column(db.Boolean, unique=False, default=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                                   onupdate=datetime.utcnow)

    def __init__(self, name, created_by_id, is_group_tab=False):
        self.name = name
        self.created_by_id = created_by_id
        self.is_group_tab = is_group_tab

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_by_id(cls, tab_id):
        return cls.query.filter_by(id=tab_id).first()

    def update_tab_status(self, new_status):
        self.status = new_status
        self.save()
