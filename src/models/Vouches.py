#src/models/Vouches.py
from sqlalchemy import Column, String, Boolean, Integer, DateTime, desc
from sqlalchemy.sql import func
import datetime

from . import Base

class Vouches(Base):

    __tablename__ = 'vouches'
    giver = Column(String(128), nullable=False)
    giver_id = Column(Integer, primary_key=True)
    receiver = Column(String(128), nullable=False)
    receiver_id = Column(Integer, primary_key=True)
    positive = Column(Boolean, nullable=False)
    given_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, data):
        '''
        Class constructor
        '''
        self.giver = data.get('giver')
        self.giver_id = data.get('giver_id')
        self.receiver = data.get('receiver')
        self.receiver_id = data.get('receiver_id')
        self.positive = data.get('positive')
        self.given_at = datetime.datetime.utcnow()

    def save(self, session):
        session.add(self)
        session.commit()

    def update(self, positive: bool, session):
        setattr(self, 'positive', positive)
        setattr(self, 'given_at', datetime.datetime.utcnow()) # change time for CD
        session.commit()

    def update_discord_id(self, giver_id: int, receiver_id: int, session):
        setattr(self, 'giver_id', giver_id)
        setattr(self, 'receiver_id', receiver_id)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f'Giver: {self.giver}\nReceiver: {self.receiver}\nPositive: {self.positive}'

    @staticmethod
    def get_vouch_named(giver: str, receiver: str, session):
        return session.query(Vouches).filter_by(giver=giver, receiver=receiver).first()

    @staticmethod
    def get_vouch(giver_id: int, receiver_id: int, session):
        return session.query(Vouches).filter_by(giver_id=giver_id, receiver_id=receiver_id).first()

    @staticmethod
    def get_all_vouches(session):
        return session.query(Vouches).all()

    @staticmethod
    def get_vouch_counts(session):
        return session.query(Vouches.giver_id).count()

    @staticmethod
    def get_history(receiver_id: int, session):
        return session.query(Vouches).filter(Vouches.receiver_id == receiver_id).all()

    @staticmethod
    def get_latest(giver_id: int, session):
        return session.query(Vouches).filter_by(giver_id=giver_id).order_by(desc('given_at')).first()
