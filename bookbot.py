# bookbot.py
# Python libraries
import discord
import os
import re

# Module Imports
from mc import mc
from pkmn import pkmn
from reviews import reviews
from roll import roll
from steam import steam
from wow import wow

# Function Imports
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

def help(received):
    response = "```\n"
    response += "Available Commands for BookBot:\n\n"
    response += "!help: Display this help text!\n"
    if received == GUILD:
        response += "!mc: Manage minecraft servers. Try !mc help for more info.\n"
        response += "!pkmn: Get the page of a pokemon. Can take stats, boop, or moves/learnlist/learnset as an argument.\n"
    response += "!reviews: Search metacritic. Can specify tv, movies, or a game console to try for a direct link.\n"
    response += "!roll: Quantum dice roller. Takes dice, bonuses, comments, e.g. '!roll 2d8+1d6+4+2 fire damage'.\n"
    response += "!steam: Search for any game on steam. Can also be activated by putting any words in {curly braces}.\n"
    response += "!wow: ☆Wow!☆\n"
    response += "```\n"
    return response

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(client.user.name + " has connected to Discord!")
    print("Connected to Server: " + guild.name + " id: (" + str(guild.id) + ")")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    modules = {
        'help': help,
        'reviews': reviews,
        'roll': roll,
        'steam': steam,
        'wow': wow
    }

    # Do not allow minecraft server management outside of book club
    if message.guild.name == GUILD:
        modules['mc'] = mc
        modules['pkmn'] = pkmn

    command = ""
    response = ""
    substring = ""

    # Attempt to parse command into command and substring
    if message.content and message.content[0] == "!":
        try:
            command, substring = message.content[1:].split(" ", 1)
        except:
            command = message.content[1:]
            pass

        # Convert command to lowercase for easier case matching
        command = command.lower()

    try:
        # Feed help module current server to know what functions should be available
        if command == "help":
            substring = message.guild.name
        # Check if the message matches a known command, and execute it
        response = modules[command](substring)
    except Exception as ex:
        # No command match, parse to see if any bot searches are embedded in the message
        game = re.search(r"\{(.*?)\}", message.content)
        if game:
            game = game.group(1)
            response = steam(game)
        else:
            pass

    if response:
        if isinstance(response, discord.Embed):
            await message.channel.send(embed=response)
        else:
            await message.channel.send(response)
    return

client.run(TOKEN)
