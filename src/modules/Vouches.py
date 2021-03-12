#src/modules/Vouches.py
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vouches:

    id = Column(Integer, primary_key=True, nullable=False)
    giver = Column(String(128), nullable=False)
    receiver = Column(String(128), nullable=False)
    positive = Column(Boolean, nullable=False)

    def __init__(self, give: str, receiver: str, positive: bool):
        '''
        Class constructor
        '''
        self.giver = giver
        self.receiver = receiver
        self.positive = positive

    def save(self, session):
        db.session.add(self)
        db.session.commit()

    def update(self, positive: bool, session):
        setattr(self, 'positive', positive)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f'Giver: {self.giver}\nReceiver: {self.receiver}\nPositive: {self.positive}'

    @staticmethod
    def get_vouch(giver: str, session):
        return session.query(User).filter_by(giver=giver, receiver=receiver).first()
