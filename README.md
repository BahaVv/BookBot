# BookBot
A chat bot that uses discord.py. Not really intended for public use, but made public for reference. Integrates a number of modules that I've found useful for various server operations and functions for friends.

bookbot.py is the primary bot application, the remaining python and shell files are modules utilized by it but kept separate for organizational purposes.

- bookbot.py: Core chatbot/command routing functionality
- mc.py,mc_serv.sh,mc_serv.txt: Minecraft server management module
- pkmn.py: Utilities to look up pocket monster information on bulbapedia
- reviews.py: Module to easily look up reviews for TV, Movies, or any game console on Metacritic
- roll.py: True random dice roller/random number generator hooked up to a quantum field sensor API
- steam.py: Module to look up games on Steam quickly
- wow.py: A silly module that constructs a decorated discord embed with a 'wow' reaction
