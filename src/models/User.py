#src/models/User.py
from sqlalchemy import Column, Integer, String, Boolean
from discord import User
from . import Base

class User(Base):

    __tablename__ = 'users'

    discord_id = Column(Integer)
    user = Column(String(128), primary_key=True, nullable=False)
    vouches = Column(Integer, nullable=False, default=0)
    '''
    # future columns
    scammer = Column(Boolean, nullable=True, default=False)
    reputable = Column(Boolean, nullable=True, default=False)
    '''

    def __init__(self, data):
        """
        Class constructor
        """
        self.discord_id = data.get('discord_id')
        self.user = data.get('user')
        self.vouches = data.get('vouches')

    def save(self, session):
        session.add(self)
        session.commit()

    def update(self, number: int, session):
        setattr(self, 'vouches', number)
        session.commit()

    def update_discord_id(self, discord_id: int, session):
        setattr(self, 'discord_id', discord_id)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f'User: {self.user}\nVouches: {self.vouches}'

    @staticmethod
    def get_user(discord_id: int, session):
        return session.query(User).filter_by(discord_id=discord_id).first()

    @staticmethod
    def get_all_users(session):
        return session.query(User).all()
