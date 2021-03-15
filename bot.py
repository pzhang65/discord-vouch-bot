# bot.py
import os
import discord
import datetime
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
    #admin_role = message.guild.roles.find()

    bot_avatar = client.user.avatar_url

    cmds = Commands(message)

    if msg.startswith('$vouchhelp'):
        #cmds = Commands(message)
        await cmds.help(bot_avatar)
        return

    if msg.startswith('$vouch'):
        #cmds = Commands(message)

        if len(message.mentions) == 0 or len(words) < 3 or words[-1] not in word_list:
                await cmds.send_error(cmds.vformat)
                return


        if message.author.id == message.mentions[0].id:
                await cmds.send_error(cmds.yourself)
                return

        else:
            user = str(message.author)
            user_avatar = message.author.avatar_url

            target = str(message.mentions[0])
            positive = Commands.check_positive(words)

            if not Commands.check_cooldown(user, session):
                await cmds.send_cooldown(cmds.cooldown)
                return

            vouch = Commands.check_duplicate_vouch(user, target, positive, session)
            # vouch returned if same user and target
            if vouch:
                old_pos = vouch.positive
                # check if old vouch is the same positive/negative as new vouch
                if old_pos == positive:
                    await cmds.send_error(cmds.dup) # cannot vouch same person twice
                    return
                else: # vouch was changed from positive -> negative or vice versa
                    Commands.change_vouch(vouch, positive, session)
                    target = User.get_user(target, session)
                    new_pos = (lambda x: "positive" if x == True else "negative")(positive)
                    old_pos = (lambda x: "negative" if x == "positive" else "positive")(new_pos)

                    await cmds.revouch(f'Changed last {old_pos} vouch to {new_pos} vouch.\n{target.user} now has {target.vouches} vouches.', user, user_avatar)
                    return

            if not User.get_user(target, session):
                Commands.create_user(target, session)

            if positive:
                pos = "positive"
            else:
                pos = "negative"

            Commands.update_user_vouch(target, positive, session)
            vouch_msg = f'{user} is giving {target} a {pos} vouch.\nZehro suck my nuts'
            await cmds.send_vouch(vouch_msg, user, user_avatar)

    if msg.startswith('$check'):
        #cmds = Commands(message)

        if len(message.mentions) == 0 or len(words) < 2:
                await cmds.send_error(cmds.cformat)
                return

        else:
            target = str(message.mentions[0])
            target_avatar = message.mentions[0].avatar_url

            user = User.get_user(target, session)

            if not user:
                await cmds.view_vouch(f'{target} has no vouches!', target, target_avatar)
                return

            msg = f'{user.user} has {user.vouches} vouches.'
            await cmds.view_vouch(msg, target, target_avatar)

    if msg.startswith('$adminvouch'):
        admin = discord.utils.get(message.author.roles, name='admin')
        if not admin:
            await cmds.send_error('You do not have admin permission.')
            return


        if len(message.mentions) == 0 or len(words) < 3:
                await cmds.send_error(cmds.aformat)
                return

        else:
            try:
                number = int(words[-1])
            except ValueError:
                await cmds.send_error('Invalid number format')
                return

            target = str(message.mentions[0])
            target_avatar = message.mentions[0].avatar_url


            user_obj = User.get_user(target, session)
            user_obj.update(number, session)

            msg = f'{user_obj.user} now has {user_obj.vouches} vouches.'
            await cmds.view_vouch(msg, user_obj.user, target_avatar)

client.run(TOKEN)
