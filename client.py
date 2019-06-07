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
		REPORT_COUNT = 5
	
		helper.running = True
		friend_values = {}
		
		await message.author.send('Finding you friends...')
		await message.channel.send('Running friend analysis...')
		
		friend_values = await finder.find_friends(message.author, message.guild)
		
		ordered_list = sorted(friend_values.items(), key=lambda x: x[1], reverse=True)
		
		report = "Your top 5 most similar people:\n\n"
		
		i = 0
		while i < REPORT_COUNT and i < len(ordered_list):
			report += "<@" + str(ordered_list[i][0]) + "> : " + '{:.1%}'.format(ordered_list[i][1]) + "\n"
			i += 1
		
		await message.author.send(report)
		await message.channel.send('Analysis complete!')
		
		helper.running = False
		
	if message.content.startswith('!~find') and helper.running:
		await message.channel.send('Currently busy!')
		
	if message.content.startswith('!~help'):
		await message.channel.send('Type `!~find` into this channel to let me find friends for you! Only one person can run this at a time.')

client.run(TOKEN_AUTH)
