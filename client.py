import discord
import helper, finder
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token_file = open("token.txt", "r") #auth token

TOKEN_AUTH = token_file.readline()
token_file.close()

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	await client.change_presence(status=discord.Status.online, activity=discord.Game(helper.idle_status))

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	if message.content.startswith('!~find') and not helper.running:
		REPORT_COUNT = 5
	
		helper.running = True
		await client.change_presence(status=discord.Status.dnd, activity=discord.Game(helper.active_status))
		
		await message.author.send("Finding you friends... (this will take a while, don't be afraid if I go offline!)")
		await message.channel.send("Running friend analysis... (this will take a while, don't be afraid if I go offline!)")
		
		friend_values = await finder.find_friends(message.author, message.guild)
		ordered_list = sorted(friend_values.items(), key=lambda x: x[1], reverse=True) # creates a list of tuples
		
		report = "Your top 5 most similar people:\n\n"
		
		i = 0
		while i < REPORT_COUNT and i < len(ordered_list):
			report += ordered_list[i][0] + " : " + '{:.1%}'.format(ordered_list[i][1]) + "\n"
			i += 1
		
		await message.author.send(report)	
		await client.change_presence(status=discord.Status.online, activity=discord.Game(helper.idle_status))
		await message.channel.send("Analysis complete!")
		
		helper.running = False
		
	if message.content.startswith("!~find") and helper.running:
		await message.channel.send("Currently busy!")
		
	if message.content.startswith("!~help"):
		await message.channel.send("Type `!~find` into this channel to let me find friends for you! Only one person can run this at a time.")
		
client.run(TOKEN_AUTH)
