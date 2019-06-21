import discord
from discord.ext import commands

import helper, finder

logger = helper.create_logger()

token_file = open("token.txt", "r") #auth token

TOKEN_AUTH = token_file.readline()
token_file.close()

client = commands.Bot(command_prefix = "!~")
client.remove_command("help") #removes the default help command

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	await client.change_presence(status = discord.Status.online, activity = helper.game_status)

@client.command(name = "find")
async def find_friends(ctx):
	if not helper.running:
		REPORT_COUNT = 5
	
		helper.running = True
		#await client.change_presence(status = discord.Status.dnd, activity = helper.active_status)
		
		await ctx.author.send("Finding you friends... (this will take a while, don't be afraid if I go offline!)")
		await ctx.send("Running friend analysis... (this will take a while, don't be afraid if I go offline!)")
		
		friend_values = await finder.find_friends(ctx.author, ctx.guild)
		ordered_list = sorted(friend_values.items(), key=lambda x: x[1], reverse=True) # creates a list of tuples
		
		#await client.connect(reconnect=True)
		
		await ctx.author.send(embed = helper.create_embed(client.user, ctx.author, REPORT_COUNT, ordered_list))	
		#await client.change_presence(status = discord.Status.online, activity = helper.idle_status) # this line causes an error for some reason (websockets.exceptions.ConnectionClosed: WebSocket connection is closed: code = 1000 (OK), no reason)
		await ctx.send("Analysis complete!")
		
		helper.running = False
		
	else:
		await ctx.send("Currently busy!")

@client.command(name = "help")
async def show_help(ctx):
	await ctx.send("Type `!~find` into this channel to let me find friends for you! Only one person can run this at a time.")
		
client.run(TOKEN_AUTH)
