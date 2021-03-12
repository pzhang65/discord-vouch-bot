import discord

class Commands:

    RED = 0xEF233C
    BLUE = 0x00A6ED
    GREEN = 0x3EC300
    YELLOW = 0xFFB400

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

    async def send_error(self, message: str):
        '''
            Sends an error message to a channel
        '''
        embed = self.new_embed(message, color=self.RED, title='Vouch Command Error!')
        await self.msg.channel.send(embed=embed)

    async def send_vouch(self, message: str):
        '''
            Sends a success message to the object channel
        '''
        embed = self.new_embed(message, color=self.GREEN, title='Vouch Applied!')
        await self.msg.channel.send(embed=embed)

    async def view_vouch(self, message: str):
        '''
            Sends a success message to the object channel
        '''
        embed = self.new_embed(message, color=self.BLUE, title='Vouch Info')
        await self.msg.channel.send(embed=embed)

    async def help(self):
        pass

    async def about(self):
        pass

    async def top(self):
        pass
