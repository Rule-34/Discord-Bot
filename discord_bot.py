import os
import time
from random import choice, randrange
# Third party
import aiohttp
import discord
from discord.ext import commands
# Own
from helper import debug_print
from config import discord_token, API_URL, r34_bot_prefix, message_channel_id

# Init
bot = commands.Bot(command_prefix=r34_bot_prefix,
                   description="Rule 34 Bot - Seeker of sauce")

# Hardcoded max_count, would probably need to use a fetch
list_of_domains = [{'name': 'rule34.xxx', 'short': 'xxx', 'max_count': 3659351},
                   {'name': 'rule34.paheal.net',
                       'short': 'paheal', 'max_count': 3532797},
                   {'name': 'danbooru.donmai.us',
                       'short': 'danbooru', 'max_count': 3806415},
                   {'name': 'gelbooru.com', 'short': 'gelbooru', 'max_count': 5164061},
                   {'name': 'e621.net', 'short': 'e621', 'max_count': 2168016}]


# -------- Helper functions -------- #


async def domain_selector(channel, domain=None):
    # Find if its a suitable domain
    if domain:
        for domain_from_list in list_of_domains:
            if domain_from_list['short'] == domain:

                domain_name = domain_from_list["name"]
                domain_short = domain_from_list['short']
                domain_random_id = randrange(domain_from_list["max_count"])

                return domain_name, domain_short, domain_random_id

        # If for ends execution empty then send error
        await send_error(channel, error_data="Not a valid domain")

    # Choose random domain
    else:
        domain = choice(list_of_domains)
        domain_name = domain["name"]
        domain_short = domain["short"]
        domain_random_id = randrange(domain["max_count"])

        return domain_name, domain_short, domain_random_id


async def fetch_api(channel, domain, id):

    # Craft URL
    url = f'{API_URL}/{domain}/single-post/?id={id}&corsProxy=false'

    try:
        # Fetch data and return it
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                if request.status == 200:
                    json = await request.json()

                    return json

                else:
                    raise ConnectionError('Request status was not correct')

    except Exception as error:
        print(f'Fetch error:\n{error}')

        await send_error(ctx, error_data=f"Could not fetch data\n{error}")

        return


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
    await bot.change_presence(activity=discord.Game(name=f'r34.app | {r34_bot_prefix}help'))


@bot.command(brief="Echoes a message")
async def say(ctx, arg):

    # Debug message
    await invoqued_by(ctx, 'Say')

    await ctx.send(arg)


@bot.command(brief="Outputs latency", description="Calculates latency of the bot connection")
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


@bot.command(aliases=['rand', 'r'], brief="Outputs random hentai from a random domain", description="Outputs random hentai from a domain, random if none selected")
async def random(ctx, domain=None):

    # Debug message
    await invoqued_by(ctx, 'Random')

    # Select domain
    domain_name, domain_short, domain_random_id = await domain_selector(ctx.channel, domain)

    # Fetch data
    data = await fetch_api(ctx, domain_short, domain_random_id)

    # Try to use low res image
    try:
        image = data[0]["low_res_file"]

    except:
        debug_print('Failed to retrieve low res file')
        image = data[0]["high_res_file"]

    # Test if image is not undefined
    if not 'https://' in image:
        await send_error(ctx, error_data=f"Image didn't have a valid url\n{image}")

        return

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
        print(f'Send error:\n{error}\n{embed.image.url, image}')

        await send_error(ctx, error_data=f"Could not reply with an image\n{error}")

        return


# -------- BOT INIT -------- #

def init():
    # Init
    print('Starting discord bot')

    bot.run(discord_token)
