from dotenv import load_dotenv
from os import getenv

# Init
load_dotenv()

# Discord credentials
discord_token = getenv('BOT_DISCORD_TOKEN')
message_channel_id = 673117213191962649

# Debugging
debug = True
