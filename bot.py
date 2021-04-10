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

word_list = ['+1', '-1']

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

    bot_avatar = client.user.avatar_url # Bot avatar for use in emb messages

    cmds = Commands(message) # Initialize command object for sending commands

    '''
    $vouchhelp sends an emb msg with description of various commands
    and how the bot operates.
    '''
    if msg.startswith('$vouchhelp'):
        await cmds.help(bot_avatar)
        return

    if msg.startswith('$vouch'):

        '''
        Proper vouches must start with $vouch followed by @mention
        and end with -1 or +1.
        '''
        if len(message.mentions) == 0 or len(words) < 3 or words[-1] not in word_list:
                await cmds.send_error(cmds.vformat)
                return

        # Self vouches are not allowed
        if message.author.id == message.mentions[0].id:
                await cmds.send_error(cmds.yourself)
                return

        else:

            user = str(message.author)
            user_avatar = message.author.avatar_url

            target = str(message.mentions[0])
            positive = Commands.check_positive(words) # Assigns boolean value to +1/-1

            '''
            Every vouch has a self generated time when saved.
            This time is checked when a user gives a vouch.
            User's last given vouch time cannot be <5 mins.
            '''
            if not Commands.check_cooldown(user, session):
                await cmds.send_cooldown(cmds.cooldown)
                return

            # Checks if user gave target a vouch before, returns the vouch if exists. Else false
            vouch = Commands.check_duplicate_vouch(user, target, positive, session)

            if vouch: # If there is existing vouch before
                old_pos = vouch.positive
                # check if existing(old) vouch is the same positive/negative as new vouch
                if old_pos == positive:
                    await cmds.send_error(cmds.dup) # new vouch cannot be same as old vouch
                    return

                else: # Change vouch from pos -> neg or vice versa
                    Commands.change_vouch(vouch, positive, session)
                    target = User.get_user(target, session)
                    new_pos = (lambda x: "+1" if x == True else "-1")(positive)
                    old_pos = (lambda x: "-1" if x == "+1" else "+1")(new_pos)

                    await cmds.revouch(f'Changed previous {old_pos} vouch to {new_pos} vouch.\n{target.user} now has {target.vouches} vouches.', user, user_avatar)
                    return

            # Check to see if vouch receiver is in user database
            if not User.get_user(target, session):
                Commands.create_user(target, session) # Create user if not found

            if positive: # Assigning literal for use in vouch_msg
                pos = "+1"
            else:
                pos = "-1"

            '''
            After vouch is created or modified, the user profile's vouch
            value gets modified and the updated user is retrieved.
            New updated vouch value gets sent out.
            '''
            Commands.update_user_vouch(target, positive, session)
            updated_user = User.get_user(target, session)
            vouch_msg = f'{user} is giving {target} a {pos} vouch.\n{target} now has {updated_user.vouches} vouches.\nTip: $check @mention history to see full vouch history.'
            await cmds.send_vouch(vouch_msg, user, user_avatar)

    '''
    Users can check other users vouches:
    $check @mention to see just vouch value
    $check @mention history to see all vouches given, their giver name and given time.
    '''
    if msg.startswith('$check'):

        if len(message.mentions) == 0 or len(words) < 2:
            await cmds.send_error(cmds.cformat)
            return

        target = str(message.mentions[0])
        target_avatar = message.mentions[0].avatar_url

        # This checks for $vouch @mention history
        if words[-1] == 'history':
            # queries vouches table and returns list of vouches given to target
            history =  Vouches.get_history(target, session)
            await cmds.send_history(history, target, target_avatar)
            return

        else: # Just check for numerical vouch value
            # Get the @mention user
            user = User.get_user(target, session)

            if not user: # if user does not exist, it means user has no vouches
                await cmds.view_vouch(f'{target} has no vouches!', target, target_avatar)
                return

            msg = f'{user.user} has {user.vouches} vouches.\nTip: $check @mention history to see full vouch history.'
            await cmds.view_vouch(msg, target, target_avatar)

    '''
    Users with the role "Admin" can manually set the vouches column in a user row
    to an integer. This however does not create vouches in the vouches table.
    '''
    if msg.startswith('$adminvouch'):
        admin = discord.utils.get(message.author.roles, name='Admin')
        # Role name has to == Admin
        if not admin:
            await cmds.send_error('You do not have Admin permission.')
            return


        if len(message.mentions) == 0 or len(words) < 3:
                await cmds.send_error(cmds.aformat)
                return

        else:
            # Last word must be representable as an integer
            try:
                number = int(words[-1])
            except ValueError:
                await cmds.send_error('Invalid number format.')
                return

            target = str(message.mentions[0])
            target_avatar = message.mentions[0].avatar_url

            user_obj = User.get_user(target, session)

            # If user doesn't have a vouch score yet, create one and set their vouch score
            if not user_obj:
                Commands.create_user(target, session)
                user_obj = User.get_user(target, session)
                user_obj.update(number, session)
                msg = f'{user_obj.user} now has {user_obj.vouches} vouches.'
                await cmds.view_vouch(msg, user_obj.user, target_avatar)

            else:
                msg = f'{user_obj.user} now has {user_obj.vouches} vouches.'
                await cmds.view_vouch(msg, user_obj.user, target_avatar)

client.run(TOKEN)
