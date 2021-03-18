#src/models/Vouches.py
from sqlalchemy import Column, String, Boolean, Integer, DateTime, desc
from sqlalchemy.sql import func
import datetime

from . import Base

class Vouches(Base):

    __tablename__ = 'vouches'
    giver = Column(String(128), primary_key=True, nullable=False)
    receiver = Column(String(128), primary_key=True, nullable=False)
    positive = Column(Boolean, nullable=False)
    given_at = Column(DateTime, default=datetime.datetime.utcnow) 

    def __init__(self, data):
        '''
        Class constructor
        '''
        self.giver = data.get('giver')
        self.receiver = data.get('receiver')
        self.positive = data.get('positive')
        self.given_at = datetime.datetime.utcnow()

    def save(self, session):
        session.add(self)
        session.commit()

    def update(self, positive: bool, session):
        setattr(self, 'positive', positive)
        setattr(self, 'given_at', datetime.datetime.utcnow()) # change time for CD
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f'Giver: {self.giver}\nReceiver: {self.receiver}\nPositive: {self.positive}'

    @staticmethod
    def get_vouch(giver: str, receiver: str, session):
        return session.query(Vouches).filter_by(giver=giver, receiver=receiver).first()

    @staticmethod
    def get_history(receiver: str, session):
        return session.query(Vouches).filter(Vouches.receiver == receiver).all()

    @staticmethod
    def get_latest(giver: str, session):
        return session.query(Vouches).filter_by(giver=giver).order_by(desc('given_at')).first()
