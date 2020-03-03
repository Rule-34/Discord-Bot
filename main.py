from argparse import ArgumentParser
from os import path, remove

# Own
from helper import debug_print
import discord_bot

# Define variables
version = 0.2


# Start
def main():

    # Initiate the parser
    parser = ArgumentParser(
        description='Rule 34 Discord Bot: modify settings on "config.py"')

    # Add arguments
    parser.add_argument("-V", "--version",
                        help="show script version and exit", action="store_true")

    # Read arguments from the command line
    args = parser.parse_args()

    # check for --version or -V
    if args.version:
        print(f"Discord Bot {version}")
        return

    # Execute bot
    discord_bot.init()

    # print('Nothing executed, exiting...')


# Actually start
if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print('\nClosing...')
        quit()
