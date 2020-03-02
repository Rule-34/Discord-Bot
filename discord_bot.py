import os
import time
from random import choice, randrange
# Third party
import requests
import discord
from discord.ext import commands
# Own
from helper import debug_print
from config import discord_token, API_URL, r34_bot_prefix, message_channel_id

# Init
bot = commands.Bot(command_prefix=r34_bot_prefix,
                   description="Rule 34 Bot - Seeker of sauce")

domains = [{'name': 'rule34.xxx', 'short': 'xxx', 'max_count': 3659351},
           {'name': 'rule34.paheal.net', 'short': 'paheal', 'max_count': 3532797},
           {'name': 'danbooru.donmai.us', 'short': 'danbooru', 'max_count': 3806415},
           {'name': 'gelbooru.com', 'short': 'gelbooru', 'max_count': 5164061},
           {'name': 'e621.net', 'short': 'e621', 'max_count': 2168016}]


# -------- Helper functions -------- #

async def send_error(ctx, error_title='An error happened', error_data=None):
    embed = discord.Embed(title=error_title)
    embed.add_field(
        name="error", value=error_data, inline=False)

    # Send response
    await ctx.send(embed=embed)


# -------- BOT EVENTS -------- #

@bot.event
async def on_ready():
    # Start message
    print(f'{bot.user} has connected to Discord!')

    # Set status
    await bot.change_presence(activity=discord.Game(name='-help'))

    # Send message
    # channel = client.get_channel(message_channel_id)  # Sauce
    # message = await channel.send('Found some hot sauce\nhttps://twitter.com/Rule34App/status/1223380540923023360?s=20')


# -------- BOT COMMANDS -------- #

# @bot.command(aliases=['h'])
# async def help(ctx):
#     await ctx.send(
#         f'''Command prefix "**{r34_bot_prefix}**"

#     **Available commands**
#     help - Shows this text
#     random <domain> - Shows a random image from

#     ''')


@bot.command()
async def say(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def ping(ctx):
    time1 = time.perf_counter()

    # Send typing message as a method to test ping
    await ctx.channel.trigger_typing()

    time2 = time.perf_counter()

    # Build embed
    embed = discord.Embed(
        title="Pong!", description=f'It took {round((time2-time1)*1000)}ms')

    # Send message
    await ctx.send(embed=embed)


@bot.command(aliases=['r', 'rand'])
async def random(ctx, domain=None):

    debug_print(f'Random: invoqued by {ctx.author.name}')

    # Choose random domain
    if not domain:
        domain = choice(domains)

    # Send typing message
    # await ctx.channel.trigger_typing()

    # Fetch data
    try:
        data = requests.get(
            f'{API_URL}/{domain["short"]}/single-post/?id={randrange(domain["max_count"])}&corsProxy=false').json()

    except Exception as error:
        print(f'Fetch:\n{error}')

        await send_error(ctx, error_title="Could not fetch image")

        return

    # Try to use low res image
    try:
        image = data[0]["low_res_file"]
    except:
        print('lol')
        image = data[0]["high_res_file"]

    # Send message
    try:
        # Create embed
        embed = discord.Embed()

        embed.add_field(
            name="Mention", value=f"Hentai for {ctx.author.mention}")

        # Set image
        embed.set_image(url=image)

        # Credit
        embed.set_footer(text=f'- {domain["name"]}')

        # Send response
        message = await ctx.send(embed=embed)

        # Add reaction
        await message.add_reaction('🥵')

    except Exception as error:
        print(f'Send:\n{error}')

        await send_error(ctx, error_title="Could not reply with an image")

        return


# -------- BOT INIT -------- #

def init():
    # Init
    print('Starting discord bot')

    bot.run(discord_token)
