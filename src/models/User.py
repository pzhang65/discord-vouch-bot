#src/modules/User.py
from marshmallow import fields, Schema
from . import db

class User(db.Model):

    __tablename__ = 'users'

    user = db.Column(db.String(128), primary_key=True, nullable=False)
    vouches = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('user')
        self.vouches = data.get('vouches')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserSchema(Schema):
    user = fields.Str(required=True)
    vouch = fields.Int(required=True)
