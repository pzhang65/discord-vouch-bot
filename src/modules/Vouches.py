#src/modules/Vouches.py
import discord
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vouches:
    format = 'Please follow this format: $vouch @user positive/negative'

    giver = Column(String(128), primary_key=True, nullable=False)
    receiver = Column(String(128), nullable=False, default=0)
    #vouchers = Column(String(128), nullable=True)

    def __init__(self, give: str, receiver: str, positive: bool):
        '''
        Class constructor
        '''
        self.giver = giver
        self.receiver = receiver
        self.positive = positive

    def save(self):
        db.session.add(self)
        db.session.commit()
