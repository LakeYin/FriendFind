import discord

token_file = open("token.txt", "r") #auth token

TOKEN_AUTH = token_file.readline()
token_file.close()

client = discord.Client()

running = False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!~find') and !running:
		running = True
        await message.author.send('Finding you friends...')
		find_friends(message.author, message.guild)
		running = False
		
	if message.content.startswith('!~find') and running:
        await message.channel.send('Currently busy!')
		
	if message.content.startswith('!~help'):
        await message.channel.send('Type ```!~find``` into this channel to let me find friends for you! Only one person can run this at a time.')
		
def find_friends(user, guild):
	user_messages = []

	for channel in guild.text_channels:
		async for message in channel.history(limit=200):
			if message.author != client.user and message.author == user:
				user_messages.add(message)
				
client.run(TOKEN_AUTH)