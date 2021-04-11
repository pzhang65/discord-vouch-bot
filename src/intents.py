#src/intents.py

import discord

'''
Enables the privileged members intent for vouch bot use
'''

intents = discord.Intents.default()
intents.members = True
