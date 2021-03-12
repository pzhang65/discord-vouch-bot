#src/modules/Vouches.py
from sqlalchemy import Column, String, Boolean, Integer
from . import Base

class Vouches(Base):

    __tablename__ = 'vouches'

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
        session.add(self)
        session.commit()

    def update(self, positive: bool, session):
        setattr(self, 'positive', positive)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f'Giver: {self.giver}\nReceiver: {self.receiver}\nPositive: {self.positive}'

    @staticmethod
    def get_vouch(giver: str, receiver: str, session):
        return session.query(Vouches).filter_by(giver=giver, receiver=receiver).first()
