# bot.py

import os
import discord
from src.modules.Vouch import Vouch
from src.modules.Embedded import Embedded


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

def get_quote():
    # deserialize json
    resp = requests.get("https://zenquotes.io/api/random").json()
    # only grab raw quote + author
    quote = resp[0]['q'] + " -" + resp[0]['a']

    return quote

def check_positive(words: list):
    if words[-1] == "positive":
        return True
    else:
        return False

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    for m in guild.members:
        print(m)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()
    words = msg.split()

    if msg.startswith('$vouch'):
        emb = Embedded(message)

        if len(message.mentions) == 0 or len(words) < 3:
                error = Embedded(message)
                await emb.send_error('Valid formats:\n$vouch @user positive\n$vouch @user negative')
                return


        if message.author.id == message.mentions[0].id:
                await emb.send_error('You cannot vouch for yourself.')
                return


        else:
            user = message.author
            target = message.mentions[0]
            positive = check_positive(words)

            vouch = Vouch(user, target, positive)
            if positive:
                pos = "positive"
            else:
                pos = "negative"

            vouch_msg = f'{user} is giving {target} a {pos} vouch.\nScotty come back'
            await emb.send_success(vouch_msg)




client.run(TOKEN)
