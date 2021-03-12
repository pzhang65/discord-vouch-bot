#src/modules/Vouch.py
import discord

class Vouches:
    format = 'Please follow this format: $vouch @user positive/negative'

    def __init__(self, user: discord.User, target: discord.User, positive: bool):
        '''
        Class constructor
        '''
        self.user = user
        self.target = target
        self.positive = positive

    def save(self):
        db.session.add(self)
        db.session.commit()
