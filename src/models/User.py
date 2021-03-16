#src/modules/User.py
from sqlalchemy import Column, Integer, String
from . import Base

class User(Base):

    __tablename__ = 'users'

    user = Column(String(128), primary_key=True, nullable=False)
    vouches = Column(Integer, nullable=False, default=0)

    def __init__(self, data):
        """
        Class constructor
        """
        self.user = data.get('user')
        self.vouches = data.get('vouches')

    def save(self, session):
        session.add(self)
        session.commit()

    def update(self, number: int, session):
        setattr(self, 'vouches', number)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f'User: {self.user}\nVouches: {self.vouches}'

    @staticmethod
    def get_user(user: str, session):
        return session.query(User).filter_by(user=user).first()
