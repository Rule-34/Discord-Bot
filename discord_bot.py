import os

import discord
from config import discord_token, message_channel_id
# print(token, sauce_channel_id)

# Init
client = discord.Client()


@client.event
async def on_ready():
    # Start message
    print(f'{client.user} has connected to Discord!')

    # Set status
    await client.change_presence(activity=discord.Game(name='finding sauce'))

    # Send message
    # channel = client.get_channel(message_channel_id)  # Sauce
    # message = await channel.send('Found some hot sauce\nhttps://twitter.com/Rule34App/status/1223380540923023360?s=20')

    # Add reaction
    # await message.add_reaction('🥵')


def init():
    # Init
    print('Starting discord bot')

    client.run(discord_token)
