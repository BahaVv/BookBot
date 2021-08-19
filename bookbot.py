# bookbot.py
import os
import discord
import re

from discord.ext import commands
from dotenv import load_dotenv
from random import seed
from random import randint

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

def help(received):
    response = "```\n"
    response += "Available Commands:\n\n"
    response += "!help: Display this help text!\n"
    response += "!pkmn: Get the page of a pokemon. Can take stats, boop, or moves/learnlist/learnset as an argument.\n"
    response += "!reviews: Search metacritic. Can specify tv, movies, or a game console to try for a direct link.\n"
    response += "!steam: Search for any game on steam. Can also be activated by putting any words in {curly braces}.\n"
    response += "!wow: ☆Wow!☆\n"
    response += "```"
    return response

def steam(received):
    # substitute spaces for url space character
    response = "https://store.steampowered.com/search/?term=" + received.replace(' ', "%20")
    return response

def pkmn(received):
    # check for non-name argument
    try:
        argument, name = received.split(" ", 1)
    except:
        argument = ""
        append = ""
        name = received
        pass

    response = ""
    name = name.lower()
    argument = argument.lower()

    # Helper function for input checking
    def input_check(name, argument):
        if argument == "stats" or argument == "stat":
            return "#Stats"
        elif argument == "learnset" or argument == "moves" or argument == "learnlist":
            return "#Learnset"
        elif argument == "boop":
            if name.lower() == "espeon":
                return 100
            else:
                if "espeon" in name.lower():
                    return 101
                return 99
        else:
            return ""

    # If we got more than one input, try to match to a function
    if argument:
        append = input_check(name, argument)
        # Check if we got a result. If not, try swapping the arguments
        if not append:
            print("hit not append")
            name, argument = argument, name
            append = input_check(name, argument)
            # Check if we got a result. If not, give up and put the variables back to normal.
            if not append:
                print ("hit not not append")
                name, argument = argument, name

    if append == 99:
        response = ":point_right: "
        append = ""
    elif append == 100:
        return "Unfortunately, I am obligated to refuse this command by my creator."
    elif append == 101:
        return "Unfortunately, crafty though you may be, I am still obligated to refuse this command."

    response += "https://bulbapedia.bulbagarden.net/wiki/" + name + "_(Pok%C3%A9mon)" + append

    return response

def reviews(received):
    # Check to see if a platform was specified
    platforms = [ "movie", "tv", "show", "shows", "360", "ios", "stadia", "gameboy", "gba", "game boy advance", "ds", "3ds",
                  "vita", "n64", "gamecube", "wii", "wii u", "switch", "dreamcast", "ps1", "playstation", "ps2", "ps3",
                  "ps4", "ps5", "xbox", "xbone", "xbox one", "xbone", "xbox series", "series", "xsx", "pc" ]

    matches = []
    for match in platforms:
        if match in received:
            matches.append(match)
    
    response = ""
    received = received.lower()
    size = len(matches)

    if size == 0:
        # return search
        response = "https://www.metacritic.com/search/all/" + received.replace(' ', "%20") + "/results"
        return response
    elif size == 1:
        # return link to game for specific platform
        platforms = {
            "game boy advance": "game-boy-advance",
            "gba": "game-boy-advance",
            "gameboy": "game-boy-advance",
            "360": "xbox-360",
            "xbone": "xbox-one",
            "xsx": "xbox-series-x",
            "ps1": "ps",
            "playstation": "ps",
            "ps2": "playstation-2",
            "ps3": "playstation-3",
            "ps4": "playstation-4",
            "ps5": "playstation-5",
            "movies": "movie",
            "show": "tv",
        }

        caught = matches[0]
        try:
            # Check if the platform matches a special case
            print("try!")
            platform = platforms[caught]
        except:
            print("except!")
            # Does not match a special case, just set directly
            platform = caught

    else:
        # return link to game for specific platform, but there is overlap
        # Whittle down to one platform. Will choose first platform if not recgonized.
        if "xbox" in received:
            # xbox, xbox 360, xbox one, or xbox series
            if "xbox one" in received:
                caught = "xbox one"
                platform = "xbox-one"
            elif "xbox 360" in received:
                caught = "xbox 360"
                platform = "xbox-360"
            elif "xbox series x" in received:
                caught = "xbox series x"
                platform = "xbox-series-x"
            elif "xbox series s" in received:
                caught = "xbox series s"
                platform = "xbox-series-x"
            elif "xbox series" in received:
                caught = "xbox series"
                platform = "xbox-series-x"
            elif "series" in received:
                caught = "series"
                platform = "xbox-series-x"
        if "wii" in received:
            caught = "wii"
            platform = "wii u"
        if "show" in received:
            caught = "shows"
            platform = "tv"

    if platform != "tv" and platform != "movie":
        platform = "game/" + platform

    received = received.replace(caught, '')
    response = "https://www.metacritic.com/" + platform + "/" + received[1:].replace(' ', '-')
    return response

def wow(received):
    seed()
    selector = randint(1, 3)

    if selector == 1:
        embed = discord.Embed(
                              color=discord.Colour.random(),
                              title='✧･ﾟ: *✧･☆Wow!☆･ﾟ✧*:･ﾟ✧',
                              url='https://youtu.be/BnTdfA5aTpY',
                              description=':sparkles:Woooooooooow!:sparkles:'
                             )
        embed.set_author(
                         name="Anime Girl", 
                         url="https://twitter.com/vgdunkey",
                         icon_url="https://cdna.artstation.com/p/assets/images/images/019/293/032/large/kiki-andriansyah-hex-y.jpg?1562838735"
                        )
        embed.set_thumbnail(
                            url="https://thumbs.dreamstime.com/b/cute-rainbow-star-vector-illustration-design-142652749.jpg"
                           )
    if selector == 2:
        embed = discord.Embed(
                              color=discord.Colour.random(),
                              title='Wow.',
                              url='https://youtu.be/mBr8mcLj9QY',
                              description='Waow.'
                             )
        embed.set_author(
                         name="wOwen Wilson", 
                         url="https://twitter.com/owenwilson1",
                         icon_url="https://pbs.twimg.com/profile_images/576225660424835073/xnZxzQVE_400x400.jpeg"
                        )
        embed.set_thumbnail(
                            url="https://media.vanityfair.com/photos/5e348a5a26aeb300090a8423/5:3/w_2000,h_1200,c_limit/owen-wilson-loki.jpg"
                           )

    if selector == 3:
        embed = discord.Embed(
                              color=discord.Colour.random(),
                              title='waow. waow. waow.',
                              url='https://youtu.be/NhYz-Zij630',
                              description="Hey I'm Owen Wilson look at my nose waow"
                             )
        embed.set_author(
                         name="Owen Noseson", 
                         url="https://twitter.com/berdyaboi",
                         icon_url="https://i.ytimg.com/vi/LtNvVYFn79Q/mqdefault.jpg"
                        )
        embed.set_thumbnail(
                            url="https://i.ytimg.com/vi/LtNvVYFn79Q/mqdefault.jpg"
                           )

    return embed

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(client.user.name + " has connected to Discord!")
    print("Connected to Server: " + guild.name + "id: (" + str(guild.id) + ")")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    modules = {
        'help': help,
        'steam': steam,
        'pkmn': pkmn,
        'reviews': reviews,
        'wow': wow,
    }

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
        # Check if the message matches a known command
        response = modules[command](substring)
    except:
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
