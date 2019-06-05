import discord
import helper, finder

token_file = open("token.txt", "r") #auth token

TOKEN_AUTH = token_file.readline()
token_file.close()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!~find') and not helper.running:
        helper.running = True
        await message.author.send('Finding you friends...')
        await finder.find_friends(message.author, message.guild)
        helper.running = False
		
    if message.content.startswith('!~find') and helper.running:
        await message.channel.send('Currently busy!')
		
    if message.content.startswith('!~help'):
        await message.channel.send('Type ```!~find``` into this channel to let me find friends for you! Only one person can run this at a time.')

client.run(TOKEN_AUTH)
