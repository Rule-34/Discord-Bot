import os
import time
# Third party
import discord
from discord.ext import commands
# Own
from helper import debug_print, invoqued_by, random_post_and_send, source_and_send, send_error
from config import discord_token, r34_bot_prefix, booru_list
from r34_shared.util.booru_utils import find_boorus_with_value_by_key

# Init
bot = commands.Bot(command_prefix=r34_bot_prefix,
                   description="Rule 34 Bot - Seeker of sauce")


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
        booru_name = reaction.message.embeds[0].footer.text[2:]
        post_id = reaction.message.embeds[0].colour.value

        # Learn short from name
        booru_short = find_boorus_with_value_by_key(
            booru_name, "name", booru_list)[0]["short"]

        await source_and_send(reaction.message.channel, booru_short, post_id)

    # Show more hentai
    elif str(reaction.emoji) == '➕':
        sent = False
        retries = 0

        while not sent:

            debug_print(retries)

            if retries >= 3:
                sent = True

            sent = await random_post_and_send(reaction.message.channel, user.mention)

            sent += 1


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


@bot.command(aliases=['rand', 'r'], brief="Outputs random hentai from a random booru", description="Outputs random hentai from a booru, random if none selected")
async def random(ctx, score=None, booru=None):

    # Debug message
    invoqued_by(ctx.author.name, 'Random')

    # Error checking
    if score:
        if not score.isdigit():
            await send_error(ctx.channel, "Thats not a valid post score!")
            return

    # Init values
    sent = False
    retries = 0

    while not sent:

        debug_print(retries)

        if retries > 2:
            sent = True
            await send_error(ctx.channel, f"Tried {retries} times but I couldn't find anything")
            return

        retries += 1

        sent = await random_post_and_send(ctx.channel, ctx.author.mention, score, booru)


# -------- BOT INIT -------- #

def init():
    # Init
    print('Starting discord bot')

    bot.run(discord_token)
