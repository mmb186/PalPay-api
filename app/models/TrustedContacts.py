from app import db

"""
    Trusted Contacts User Table
"""

#
# class TrustedContacts(db.Model):
#     __tablename__ = 'TrustedContact'
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
#     contact_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
#
#     def __init__(self, user_id, contact_id):
#         self.user_id = user_id
#         self.contact_id = contact_id
#
#     def save(self):
#         db.session.add(self)
#         db.session.commit()
#         return self


# TrustedContacts = db.Table(
#     'trusted_contacts',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('contact_id', db.Integer, db.ForeignKey('users.id'))
# )
