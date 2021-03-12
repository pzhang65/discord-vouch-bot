# bot.py
import os
import discord
from src.models import Session
from src.models.User import User
from src.models.Vouches import Vouches
from src.modules.Commands import Commands


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

# Create a session using sessionmaker to connect with DB
session = Session()

word_list = ['positive', 'negative']

def check_positive(words: list):
    if words[-1] == "positive":
        return True
    else:
        return False

def create_user(user: str, session):
    data = {'user': user, 'vouches': 0}
    user_obj = User(data)
    user_obj.save(session)
    return True

def check_duplicate_vouch(giver: str, receiver: str, positive: bool, session):
    # Returns none if no vouch matches giver, receiver filter
    vouch = Vouches.get_vouch(giver, receiver, session)
    if vouch:
        return True # Cannot give more than 1 vouch to the same user
    else:
        # Creates vouch and saves to db
        vouch_obj = Vouches(giver, receiver, positive)
        vouch_obj.save(session)

        return False

def update_vouch(target: str, positive: bool, session):
    user_obj = User.get_user(target, session)
    if positive:
        user_obj.vouches += 1
    else:
        user_obj.vouches -= 1
        
    user_obj.update(user_obj.vouches, session)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()
    words = msg.split()

    if msg.startswith('$vouch'):
        cmds = Commands(message)

        if len(message.mentions) == 0 or len(words) < 3 or words[-1] not in word_list:
                await cmds.send_error(cmds.vformat)
                return


        if message.author.id == message.mentions[0].id:
                await cmds.send_error(cmds.yourself)
                return

        else:
            user = str(message.author)
            target = str(message.mentions[0])
            positive = check_positive(words)

            if check_duplicate_vouch(user, target, positive, session):
                await cmds.send_error(cmds.dup)
                return

            if not User.get_user(target, session):
                create_user(target, session)

            if positive:
                pos = "positive"
            else:
                pos = "negative"

            update_vouch(target, positive, session)
            vouch_msg = f'{user} is giving {target} a {pos} vouch.\nZehro suck my nuts'
            await cmds.send_vouch(vouch_msg)

    if msg.startswith('$check'):
        cmds = Commands(message)

        if len(message.mentions) == 0 or len(words) < 2:
                await cmds.send_error(cmds.cformat)
                return

        else:
            target = str(message.mentions[0])
            user = User.get_user(target, session)

            if not user:
                await cmds.view_vouch(f'{target} has no vouches!')
                return

            msg = f'{user.user} has {user.vouches} vouches.'
            await cmds.view_vouch(msg)



client.run(TOKEN)
