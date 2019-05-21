import discord

token_file = (“token.txt”, “r”) # Retrieved from browser local storage

TOKEN_AUTH = file.readline()

client = discord.Client()

client.run(TOKEN_AUTH, bot=False)