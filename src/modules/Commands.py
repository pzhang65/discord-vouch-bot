#src/modules/Commands.py
import discord
import datetime
from src.models.User import User
from src.models.Vouches import Vouches

class Commands:

    RED = 0xEF233C
    BLUE = 0x00A6ED
    GREEN = 0x3EC300
    YELLOW = 0xFFB400
    vformat = 'Valid formats:\n$vouch @user +1\n$vouch @user -1\n$vouchhelp for more info'
    aformat = 'Valid formats:\n$adminvouch @user number\n$vouchhelp for more info'
    cformat = 'Valid formats:\n$check @user\n$check @user history\n$vouchhelp for more info'
    yourself = 'You cannot vouch for yourself.\n$vouchhelp for more info'
    dup = 'Cannot give a duplicate vouch to the same user.\n$vouchhelp for more info'
    cooldown = 'Please wait 5 mins between every vouch.\n$vouchhelp for more info'

    def __init__(self, msg : discord.Message):
        self.msg = msg

    def new_embed(self, description: str, color: hex, title: str = 'Vouch Bot') -> discord.Embed:
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
        '''
        Assigns boolean value corresponding to +1/-1
        '''
        if words[-1] == "+1":
            return True
        else:
            return False

    @staticmethod
    def update_user_vouch(target_id: int, positive: bool, session):
        '''
        Get user first from database, then update vouch number
        '''
        user_obj = User.get_user(target_id, session)
        if positive:
            user_obj.vouches += 1
        else:
            user_obj.vouches -= 1

        user_obj.update(user_obj.vouches, session)

    @staticmethod
    def change_vouch(target_id: int, vouch: Vouches, positive: bool, session):
        '''
        Update vouch to True/False for +1/-1
        Then update user's vouch value in Users table twice
        since +1 -> -1 is a difference of 2 and vice versa
        '''
        vouch.update(positive, session)
        # update_user_vouch twice because -1 -> +1 = 2
        Commands.update_user_vouch(target_id, positive, session)
        Commands.update_user_vouch(target_id, positive, session)

    @staticmethod
    def check_duplicate_vouch(giver_id: int, receiver_id: int, positive: bool, session):
        '''
        Query vouches table to find a vouch with specified giver/receiver
        If found, return the vouch for manipulation
        else create the vouch and save to vouches table
        '''
        # Returns None if no vouch matches giver, receiver filter
        vouch = Vouches.get_vouch(giver_id, receiver_id, session)

        # If a vouch is found that matches, return the vouch
        if vouch:
            return vouch

        else:
            return False

    @staticmethod
    def check_cooldown(giver_id: int, session):
        '''
        Find the most recently given vouch from a user
        If there is no vouch that matches giver, then return True
        If there is a vouch found check the time
        Make sure it's been 5 minutes since it was given using given_at column
        '''
        vouch_obj = Vouches.get_latest(giver_id, session)
        # If never given a vouch then there is no cd
        if not vouch_obj:
            return True

        td = datetime.datetime.utcnow() - vouch_obj.given_at
        if td.total_seconds() > 300: # more than 30 mins
            return True
        else:
            return False # 5 min cd not up

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

    async def view_vouch(self, message: str, user_id: int, user: str, avatar):
        '''
        Sends a success message to the object channel
        '''
        embed = self.new_embed(message, color=self.BLUE, title='Vouch Info')
        embed.set_author(name=user, icon_url=avatar)
        embed.set_footer(text=f'Discord ID: {user_id}')
        await self.msg.channel.send(embed=embed)

    async def revouch(self, message: str, user: str, avatar):
        '''
        Sends a vouch changing message to object channel
        '''
        embed = self.new_embed(message, color=self.YELLOW, title='Changing Existing Vouch...')
        embed.set_author(name=user, icon_url=avatar)
        await self.msg.channel.send(embed=embed)

    async def send_cooldown(self, message: str):
        '''
        Sends a wait cooldown message to object channel
        '''
        embed = self.new_embed(message, color=self.YELLOW, title='Vouching Cooldown')
        await self.msg.channel.send(embed=embed)

    async def send_history(self, vouches: list, user:str, avatar):
        '''
        Sends the Discord ID of all people who gave the target user a vouch
        Queried from vouches table and includes date given and +1/-1
        '''
        embed = self.new_embed(description='', color=self.BLUE, title='Vouch History')
        for x in vouches:
            if x.positive:
                mark = '✅'
            else:
                mark = '⛔'
            date_time = x.given_at.strftime("%m/%d/%Y\n%H:%M:%S  UTC")
            embed.add_field(name=f'{mark} {x.giver}', value=f'Received: {date_time}')

        embed.set_author(name=user, icon_url=avatar)
        await self.msg.channel.send(embed=embed)

    async def help(self, avatar):
        '''
        Sends a help/info message relating to the bot, it's features and commands.
        '''
        embed = self.new_embed(description='Developed by Ess#0977, DM ideas/bugs to me.', color=self.BLUE, title='')
        embed.add_field(name='Features', value='Users can give and check +1 or -1 vouches to other users.\nVouches are stored in a database and are tied to Discord username (NOT server nickname).')
        embed.add_field(name='Giving ($vouch)', value='A user can only give 1 vouch per 5 mins.\nYou CANNOT give duplicate vouches to the same user.\nPrevious vouches CAN be changed from positive to negative and vice versa.\nVouches can be only given in the #vouches channels.')
        embed.add_field(name='Checking ($check)', value="Check user's vouch score with a @mention.\n$check @mention history to check from whom the vouches came from")
        embed.set_author(name='Vouch Bot v1.5.0', icon_url=avatar)
        await self.msg.channel.send(embed=embed)

    async def send_message(self, message: str):
        embed = self.new_embed(message, title='', color=self.YELLOW)
        await self.msg.channel.send(embed=embed)

    async def about(self):
        pass

    async def top(self):
        pass
