# bot.py
import os
import discord
import datetime
from src.models import Session
from src.models.User import User
from src.models.Vouches import Vouches
from src.modules.Commands import Commands
from src.intents import intents


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=intents)

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
    Finds the unique discord id of all users in User table
    and updates 'discord_id' column.
    '''
    if msg.startswith('$convertall'):
        user_dict = User.get_all_users(session)

        await cmds.send_message('Querying users tables')
        await cmds.send_message(f'Starting conversion on {len(user_dict)} users...')
        for u in user_dict:
            username = u.user
            user = message.guild.get_member_named(username)
            if user:
                user_obj = User.get_user_named(username, session)
                user_obj.update_discord_id(user.id, session)
                await cmds.send_message(f'Linked {username} with Discord Id: {user.id}')
            else:
                await cmds.send_message(f"{username} not found in server!")
        await cmds.send_message("Users conversion complete!")

        vouch_dict = Vouches.get_all_vouches(session)

        await cmds.send_message('Querying vouches table')
        await cmds.send_message(f'Starting conversion on {len(vouch_dict)} vouches...')
        for v in vouch_dict:
            giver_name = v.giver
            receiver_name = v.receiver

            giver = message.guild.get_member_named(giver_name)
            receiver = message.guild.get_member_named(receiver_name)

            if giver and receiver:
                vouch = Vouches.get_vouch_named(giver_name, receiver_name, session)
                vouch.update_discord_id(giver.id, receiver.id, session)
                await cmds.send_message(f"giver:{giver_name} and receiver:{receiver_name} \
                    vouch succesfully updated.")
            else:
                await cmds.send_message(f"giver:{giver_name} or receiver:{receiver_name} \
                    not found in server!")
        await cmds.send_message("Vouches conversion complete!")
        return

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
            user_id = int(message.author.id)
            user_avatar = message.author.avatar_url


            target = str(message.mentions[0])
            target_id = int(message.mentions[0].id)
            positive = Commands.check_positive(words) # Assigns boolean value to +1/-1

            '''
            Every vouch has a self generated time when saved.
            This time is checked when a user gives a vouch.
            User's last given vouch time cannot be <5 mins.
            '''
            # check_cooldown() returns False if cooldown not up
            if not Commands.check_cooldown(user_id, session):
                await cmds.send_cooldown(cmds.cooldown)
                return

            # Checks if user gave target a vouch before, returns the vouch if exists. Else false
            vouch = Commands.check_duplicate_vouch(user_id, target_id, positive, session)

            if vouch: # If there is existing vouch before
                old_pos = vouch.positive
                # check if existing(old) vouch is the same positive/negative as new vouch
                if old_pos == positive:
                    await cmds.send_error(cmds.dup) # new vouch cannot be same as old vouch
                    return

                else: # Change vouch from pos -> neg or vice versa
                    Commands.change_vouch(target_id, vouch, positive, session)
                    target = User.get_user(target_id, session)
                    new_pos = (lambda x: "+1" if x == True else "-1")(positive)
                    old_pos = (lambda x: "-1" if x == "+1" else "+1")(new_pos)

                    await cmds.revouch(f'Changed previous {old_pos} vouch to {new_pos} vouch.\n\
                        {target.user} now has {target.vouches} vouches.', user, user_avatar)
                    return

            # If there is no duplicate vouch, create one and save to db
            else:
                data = {'giver': user, 'giver_id': user_id, 'receiver': target, 'receiver_id': target_id, 'positive': positive}
                vouch = Vouches(data)
                vouch.save(session)

            # Check to see if vouch receiver is in user database
            if not User.get_user(target_id, session):
                # Create a new user and save to db if receiver is not in db
                new_user = User({'discord_id': target_id, 'user': target, 'vouches': 0})
                new_user.save(session)

            if positive: # Assigning literal for use in vouch_msg
                pos = "+1"
            else:
                pos = "-1"

            '''
            After vouch is created or modified, the user profile's vouch
            value gets modified and the updated user is retrieved.
            New updated vouch value gets sent out.
            '''
            Commands.update_user_vouch(target_id, positive, session)
            updated_user = User.get_user(target_id, session)

            vouch_msg = f'{user} is giving {target} a {pos} vouch.\n{target} now has {updated_user.vouches} vouches.\n\
                Tip: $check @mention history to see full vouch history.'
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
        target_id = int(message.mentions[0].id)
        target_avatar = message.mentions[0].avatar_url

        # This checks for $vouch @mention history
        if words[-1] == 'history':
            # queries vouches table and returns list of vouches given to target
            history =  Vouches.get_history(target_id, session)
            await cmds.send_history(history, target_id, target, target_avatar)
            return

        else: # Just check for numerical vouch value
            # Get the @mention user
            user = User.get_user(target_id, session)

            if not user: # if user does not exist, it means user has no vouches
                await cmds.view_vouch(f'{target} has no vouches!', target_id, target, target_avatar)
                return

            msg = f'{user.user} has {user.vouches} vouches.\n\
                Tip: $check @mention history to see full vouch history.'
            await cmds.view_vouch(msg, target_id, target, target_avatar)

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
            target_id = int(message.mentions[0].id)
            target_avatar = message.mentions[0].avatar_url

            user = User.get_user(target_id, session)

            # If user doesn't have a vouch score yet, create the user and set their vouch score
            if not user:
                new_user = User({'discord_id': target_id, 'user': target, 'vouches': number})
                new_user.save(session)

                msg = f'{new_user.user} now has {new_user.vouches} vouches.'
                await cmds.view_vouch(msg, new_user.user, target_avatar)

            else:
                user.vouches = number
                user.save(session)
                msg = f'{user.user} now has {user.vouches} vouches.'
                await cmds.view_vouch(msg, user.user, target_avatar)


client.run(TOKEN)
