import discord
import datetime
from src.models.User import User
from src.models.Vouches import Vouches

class Commands:

    RED = 0xEF233C
    BLUE = 0x00A6ED
    GREEN = 0x3EC300
    YELLOW = 0xFFB400
    vformat = 'Valid formats:\n$vouch @user positive\n$vouch @user negative'
    aformat = 'Valid formats:\n$adminvouch @user number'
    cformat = 'Valid formats:\n$check @user'
    yourself = 'You cannot vouch for yourself.'
    dup = 'Cannot vouch for the same user more than once.'
    cooldown = 'Please wait 30 mins between every vouch.'

    def __init__(self, msg : discord.Message):
        self.msg = msg

    def new_embed(self, description: str, color: hex, title: str = 'vouch bot') -> discord.Embed:
        '''
            Creates a new Embed object
        '''
        return discord.Embed(
            title=title,
            description=description,
            color=color,
        )

    @staticmethod
    def check_positive(words: list):
        if words[-1] == "positive":
            return True
        else:
            return False
    @staticmethod
    def create_user(user: str, session):
        data = {'user': user, 'vouches': 0}
        user_obj = User(data)
        user_obj.save(session)
        return True
    @staticmethod
    def update_user_vouch(target: str, positive: bool, session):
        user_obj = User.get_user(target, session)
        if positive:
            user_obj.vouches += 1
        else:
            user_obj.vouches -= 1

        user_obj.update(user_obj.vouches, session)

    @staticmethod
    def change_vouch(vouch: Vouches, positive: bool, session):
        vouch.update(positive, session)
        # update_user_vouch twice because -1 -> +1 = 2
        Commands.update_user_vouch(vouch.receiver, positive, session)
        Commands.update_user_vouch(vouch.receiver, positive, session)

    @staticmethod
    def check_duplicate_vouch(giver: str, receiver: str, positive: bool, session):
        # Returns none if no vouch matches giver, receiver filter
        vouch = Vouches.get_vouch(giver, receiver, session)
        if vouch:
            return vouch

        else:
            # Creates vouch and saves to db
            data = {'giver': giver, 'receiver': receiver, 'positive': positive}
            vouch_obj = Vouches(data)
            vouch_obj.save(session)

            return False

    @staticmethod
    def check_cooldown(giver: str, session):
        vouch_obj = Vouches.get_latest(giver, session)
        if not vouch_obj: # If never vouched then there is no cd
            return True

        td = datetime.datetime.utcnow() - vouch_obj.given_at
        if td.total_seconds() > 1800: # more than 30 mins
            return True
        else:
            return False # 30 min cd not up

    async def send_error(self, message: str):
        '''
            Sends an error message to a channel
        '''
        embed = self.new_embed(message, color=self.RED, title='Vouch Command Error!')
        await self.msg.channel.send(embed=embed)

    async def send_vouch(self, message: str, user: str, avatar):
        '''
            Sends a success message to the object channel
        '''
        embed = self.new_embed(message, color=self.GREEN, title='Vouch Applied!')
        embed.set_author(name=user, icon_url=avatar)
        await self.msg.channel.send(embed=embed)

    async def view_vouch(self, message: str, user: str, avatar):
        '''
            Sends a success message to the object channel
        '''
        embed = self.new_embed(message, color=self.BLUE, title='Vouch Info')
        embed.set_author(name=user, icon_url=avatar)
        await self.msg.channel.send(embed=embed)

    async def revouch(self, message: str, user: str, avatar):
        embed = self.new_embed(message, color=self.YELLOW, title='Changing Existing Vouch...')
        embed.set_author(name=user, icon_url=avatar)
        await self.msg.channel.send(embed=embed)

    async def send_cooldown(self, message: str):
        embed = self.new_embed(message, color=self.YELLOW, title='Vouching Cooldown')
        await self.msg.channel.send(embed=embed)

    async def help(self, avatar):
        embed = self.new_embed(description='Developed by Ess#0977, DM ideas/bugs to me.', color=self.BLUE, title='')
        embed.add_field(name='Features', value='Users can give (and check) positive (+1) or negative (-1) vouches to other users.\nVouches are stored in a database and are tied to Discord username (NOT server nickname).')
        embed.add_field(name='Giving ($vouch)', value='A user can only give 1 vouch per 30 mins.\nYou CANNOT give duplicate vouches to the same user.\nPrevious vouches CAN be changed from positive to negative and vice versa.\nVouches can be only given in the #vouches channels.')
        embed.add_field(name='Checking ($check)', value='Every user have a numerical vouch score that starts from 0.\nVouches can be checked in any text channel but the user must be pinged.')
        embed.set_author(name='Vouch Bot', icon_url=avatar)
        await self.msg.channel.send(embed=embed)

    async def about(self):
        pass

    async def top(self):
        pass
