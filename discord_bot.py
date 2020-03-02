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

list_of_domains = [{'name': 'rule34.xxx', 'short': 'xxx', 'max_count': 3659351},
                   {'name': 'rule34.paheal.net',
                       'short': 'paheal', 'max_count': 3532797},
                   {'name': 'danbooru.donmai.us',
                       'short': 'danbooru', 'max_count': 3806415},
                   {'name': 'gelbooru.com', 'short': 'gelbooru', 'max_count': 5164061},
                   {'name': 'e621.net', 'short': 'e621', 'max_count': 2168016}]


# -------- Helper functions -------- #

async def send_error(ctx, error_title='Error', error_data=None):
    embed = discord.Embed(title=error_title)
    embed.add_field(
        name="Message", value=error_data, inline=False)

    # Send response
    await ctx.send(embed=embed)


async def invoqued_by(ctx, command=None):
    debug_print(f'{command}: invoqued by {ctx.author.name}')


# -------- BOT EVENTS -------- #

@bot.event
async def on_ready():
    # Start message
    print(f'{bot.user} has connected to Discord!')

    # Set status
    await bot.change_presence(activity=discord.Game(name='-help'))


@bot.command()
async def say(ctx, arg):

    # Debug message
    await invoqued_by(ctx, 'Ping')

    await ctx.send(arg)


@bot.command()
async def ping(ctx):

    # Debug message
    await invoqued_by(ctx, 'Ping')

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

    # Debug message
    await invoqued_by(ctx, 'Ping')

    # Find if its a suitable domain
    if domain:
        for domain_from_list in list_of_domains:
            if domain_from_list['short'] == domain:

                domain_name = domain_from_list["name"]
                domain_short = domain_from_list['short']
                domain_random_id = randrange(domain_from_list["max_count"])
                break

    # Choose random domain
    else:
        domain = choice(list_of_domains)
        domain_name = domain["name"]
        domain_short = domain["short"]
        domain_random_id = randrange(domain["max_count"])

    # Send typing message
    # await ctx.channel.trigger_typing()

    # Fetch data
    try:
        data = requests.get(
            f'{API_URL}/{domain_short}/single-post/?id={domain_random_id}&corsProxy=false').json()

    except Exception as error:
        print(f'Fetch:\n{error}')

        await send_error(ctx, error_title="Could not fetch image")

        return

    # Try to use low res image
    try:
        image = data[0]["low_res_file"]
    except:
        image = data[0]["high_res_file"]

        debug_print('Failed to retrieve low res file')

    # Send message
    try:
        # Create embed
        embed = discord.Embed()

        embed.add_field(
            name="Mention", value=f"Hentai for {ctx.author.mention}")

        # Set image
        embed.set_image(url=image)

        # Credit
        embed.set_footer(text=f'- {domain_name}')

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
