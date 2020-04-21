import discord
from random import choice, randrange
from requests import get

from config import debug, API_URL, booru_list, booru_score

from r34_shared.util.booru_utils import find_boorus_with_value_by_key


# -------- Helper functions -------- #
async def random_post_and_send(channel, mention, score=None, booru=None):

    # Set score to config booru_score if undefined
    if not score:
        score = booru_score

    if booru:
        booruData = find_boorus_with_value_by_key(booru, "short", booru_list)

        if booruData:
            random_name = booruData[0]['name']
            random_short = booruData[0]['short']

        else:
            await send_error(channel, "Unknown booru!")
            return True

    else:
        # Select a random booru
        random_name, random_short = randomBooru()

    try:
        # Get random media from a random booru
        debug_print('Fetching post')
        data = http_get(
            f"{API_URL}/{random_short}/random-post?score={score}&cacheBreaker={randrange(99999999999)}")  # TEMPORAL CACHE BREAKER

        data = data.json()

        post_id, file_url = extractAttr(data)

        await send_embed(channel, mention, random_name, post_id, file_url)

        return True

    except Exception as error:
        print(f"getAndProcessPost Error: {error}")
        return False


async def source_and_send(channel, booru_short, post_id):

    # Fetch data
    data = http_get(f"{API_URL}/{booru_short}/single-post?id={post_id}")

    data = data.json()

    if 'source' in data[0]:
        source = data[0]['source']

    else:
        source = 'No source available, sorry!'

    # Create embed and send it
    embed = discord.Embed()

    embed.add_field(
        name="Source", value=source)

    await channel.send(embed=embed)


async def send_embed(channel, mention, booru_name, post_id, file_url):

    # Test if image is not undefined
    if not file_url.startswith('http'):
        debug_print(f"File didn't have a valid url\n{file_url}")
        raise Exception

    # Create embed
    embed = discord.Embed()

    embed.add_field(
        name="Mention", value=f"Hentai for {mention}")

    # Set image
    embed.set_image(url=file_url)

    # Set domain ID
    embed.colour = post_id

    # Credit
    embed.set_footer(text=f'- {booru_name}')

    # Send response
    message = await channel.send(embed=embed)

    # Add "hot" reaction
    # await message.add_reaction('🥵')

    # Add "source" reaction
    await message.add_reaction('🌶')

    # Add "give me more" reaction
    await message.add_reaction('➕')


async def send_error(channel, error_data, error_title='Error'):
    embed = discord.Embed(title=error_title)
    embed.add_field(
        name="Message", value=error_data, inline=False)

    # Send response
    await channel.send(embed=embed)


def randomBooru():
    random_booru = choice(booru_list)

    random_name = random_booru['name']
    random_short = random_booru['short']

    return random_name, random_short


def extractAttr(data):

    post_id = data[0]["id"]

    try:
        file_url = data[0]["low_res_file"]

    except:
        debug_print('Failed to retrieve low res file')
        file_url = data[0]["high_res_file"]

    return post_id, file_url

#
# General Utilities
#


def http_get(url):
    debug_print(url)

    request = get(url)

    request.raise_for_status()

    return request


def debug_print(text):
    if debug:
        print(f'DEBUG: {text}\n')


def invoqued_by(name, command=None):
    debug_print(f'{command}: invoqued by {name}')
