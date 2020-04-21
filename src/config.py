from dotenv import load_dotenv
from os import getenv

from r34_shared.util.booru_utils import remove_boorus_with_values_by_key, booru_list_nsfw

# Init
load_dotenv()
r34_bot_prefix = '-'

# Discord credentials
discord_token = getenv('BOT_DISCORD_TOKEN')
# message_channel_id = 673117213191962649

# Rule 34 API
API_URL = "https://rule-34-api.herokuapp.com"


# Debugging
debug = True


# Booru configuration
booru_score = 50

blacklisted_short = ["lolibooru"]

booru_list = remove_boorus_with_values_by_key(
    blacklisted_short, "short", booru_list_nsfw)

# print(nsfw_list)
