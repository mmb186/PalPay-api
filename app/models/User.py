from datetime import datetime

from app import db, bcrypt


class User(db.Model):
    """
        User Table Schema
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __inti__(self, email, public_id, password, first_name, last_name):
        self.email = email
        self.public_id = public_id
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<id {self.id}>'

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def generate_hash(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

