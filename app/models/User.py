from datetime import datetime

from app import db, bcrypt


trusted_contacts = db.Table(
    'trusted_contacts',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('users.id'))
)


class User(db.Model):
    """
        User Table Schema
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_time = db.Column(db.DateTime, nullable=False,
                                   default=datetime.utcnow, onupdate=datetime.utcnow)
    trusted_contacts = db.relationship(
        'User',
        secondary=trusted_contacts,
        primaryjoin=(trusted_contacts.c.user_id == id),
        secondaryjoin=(trusted_contacts.c.contact_id == id),
        backref=db.backref('trusted_contacts_ref', lazy='dynamic'),
        lazy='dynamic'
    )

    def __inti__(self, email, public_id, password, first_name, last_name, username):
        self.email = email
        self.public_id = public_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    def __repr__(self):
        return f'<id {self.id}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def generate_hash(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def add_contact(self, user):
        if not self.is_already_contact(user):
            self.trusted_contacts.append(user)

    def remove_contact(self, user):
        if self.is_already_contact(user):
            self.trusted_contacts.remove(user)

    def is_already_contact(self, user):
        return self.trusted_contacts.filter(
            trusted_contacts.c.contact_id == user.id).count() > 0
