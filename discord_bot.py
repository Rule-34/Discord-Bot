import os
import time
from random import choice, randrange
# Third party
import aiohttp
import discord
from discord.ext import commands
# Own
from helper import list_of_domains, find_domain_by_selector, debug_print, invoqued_by
from config import discord_token, API_URL, r34_bot_prefix, message_channel_id

# Init
bot = commands.Bot(command_prefix=r34_bot_prefix,
                   description="Rule 34 Bot - Seeker of sauce")


# -------- Helper functions -------- #


async def random_domain(channel, domain=None, selector='short'):
    # Find if its a suitable domain
    if domain:
        domain_dic = find_domain_by_selector(domain, selector)

        domain_name = domain_dic["name"]
        domain_short = domain_dic["short"]
        domain_random_id = randrange(domain_dic["max_count"])

        if domain_dic:
            return domain_name, domain_short, domain_random_id

        # If for ends execution empty then send error
        await send_error(channel, error_data="Not a valid domain")

    # Choose random domain
    else:
        domain_dic = choice(list_of_domains)
        domain_name = domain_dic["name"]
        domain_short = domain_dic["short"]
        domain_random_id = randrange(domain_dic["max_count"])

        return domain_name, domain_short, domain_random_id


async def fetch_api(channel, domain, id):

    # Craft URL
    url = f'{API_URL}/{domain}/single-post/?id={id}&corsProxy=false'

    try:
        # Fetch data and return it
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                if request.status == 200:
                    api_request = await request.json()

                    # Error handling
                    if not api_request:
                        raise ConnectionError('No data received')

                    return api_request

                else:
                    raise ConnectionError('Request status was not correct')

    except Exception as error:
        print(f'Fetch error:\n{error}')

        await send_error(channel, error_data=f"Could not fetch data\n{error}")

        return None


async def send_embed(channel, mention, api_request, domain_name, domain_random_id):

    # Try to use low res image
    try:
        image = list(api_request)[0]["low_res_file"]

    except:
        debug_print('Failed to retrieve low res file')
        image = list(api_request)[0]["high_res_file"]

    # Test if image is not undefined
    if not image.startswith('http'):
        await send_error(channel, error_data=f"Image didn't have a valid url\n{image}")

        return

    # Send message
    try:
        # Create embed
        embed = discord.Embed()

        embed.add_field(
            name="Mention", value=f"Hentai for {mention}")

        # Set image
        embed.set_image(url=image)

        # Set domain ID
        embed.colour = domain_random_id

        # Credit
        embed.set_footer(text=f'- {domain_name}')

        # Send response
        message = await channel.send(embed=embed)

        # Add "hot" reaction
        # await message.add_reaction('🥵')

        # Add "source" reaction
        await message.add_reaction('🌶')

        # Add "give me more" reaction
        await message.add_reaction('➕')

    except Exception as error:
        print(f'Send error:\n{error}\n{embed.image.url, image}')

        await send_error(channel, error_data=f"Could not reply with an image\n{error}")

        return


async def send_error(channel, error_title='Error', error_data=None):
    embed = discord.Embed(title=error_title)
    embed.add_field(
        name="Message", value=error_data, inline=False)

    # Send response
    await channel.send(embed=embed)


# -------- BOT EVENTS -------- #

@bot.event
async def on_ready():
    # Start message
    print(f'{bot.user} has connected to Discord!')

    # Set status
    await bot.change_presence(activity=discord.Game(name=f'r34.app | {r34_bot_prefix}help'))


@bot.event
async def on_reaction_add(reaction, user):
    # Skip messages from the bot
    if user == bot.user:
        return
    # Skip messages from other bots
    if not reaction.message.author == bot.user:
        return

    invoqued_by(user, 'Reaction')
    # print(f'{reaction} - {user}\n{reaction.message}')

    # Show source
    if str(reaction.emoji) == '🌶':

        # Get variables
        _domain_name = reaction.message.embeds[0].footer.text[2:]
        _domain_random_id = reaction.message.embeds[0].colour.value

        # Learn short from name
        _domain_short = await random_domain(reaction.message.channel, _domain_name, 'name')

        # Fetch data
        api_request = await fetch_api(reaction.message.channel, _domain_short[1], _domain_random_id)

        if list(api_request)[0]['source']:
            _source = list(api_request)[0]['source']

        else:
            _source = 'No source available, sorry!'

        # Create embed and send it
        embed = discord.Embed()

        embed.add_field(
            name="Source", value=_source)

        await reaction.message.channel.send(embed=embed)

    # Show more hentai
    elif str(reaction.emoji) == '➕':

        # Select domain
        domain_name, domain_short, domain_random_id = await random_domain(reaction.message.channel)

        # Fetch data
        api_request = await fetch_api(reaction.message.channel, domain_short, domain_random_id)

        if not api_request:
            return

        # Send embed
        await send_embed(reaction.message.channel, user.mention, api_request, domain_name, domain_random_id)


@bot.command(brief="Echoes a message")
async def say(ctx, arg):

    # Debug message
    invoqued_by(ctx.author.name, 'Say')

    await ctx.send(arg)


@bot.command(brief="Outputs latency", description="Calculates latency of the bot connection")
async def ping(ctx):

    # Debug message
    invoqued_by(ctx.author.name, 'Ping')

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
    invoqued_by(ctx.author.name, 'Random')

    # Select domain
    domain_name, domain_short, domain_random_id = await random_domain(ctx.channel, domain)

    # Fetch data
    api_request = await fetch_api(ctx.channel, domain_short, domain_random_id)

    if not api_request:
        return

    # Send embed
    await send_embed(ctx.channel, ctx.author.mention, api_request, domain_name, domain_random_id)


# -------- BOT INIT -------- #

def init():
    # Init
    print('Starting discord bot')

    bot.run(discord_token)
