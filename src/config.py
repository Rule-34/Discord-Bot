from dotenv import load_dotenv
from os import getenv

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
