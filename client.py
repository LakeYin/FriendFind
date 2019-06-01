import discord
import status
import numpy

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

    if message.content.startswith('!~find') and not status.running:
        status.running = True
        await message.author.send('Finding you friends...')
        await find_friends(message.author, message.guild)
        status.running = False
		
    if message.content.startswith('!~find') and status.running:
        await message.channel.send('Currently busy!')
		
    if message.content.startswith('!~help'):
        await message.channel.send('Type ```!~find``` into this channel to let me find friends for you! Only one person can run this at a time.')
		
async def find_friends(user, guild):
	word_list = []
	word_map = {}
	
	user_messages = []
	user_ints = []
	
	for channel in guild.text_channels:
		try:
			async for message in channel.history().filter(lambda m: not m.author.bot and not m.attachments): #filters out messages from bots and messages with attachments
				if message.author == user:
					user_messages.append(message.clean_content)
		
		except:
			print("Could not view " + channel.name)
				
	#print(user_messages)
	
	def get_number(word): # maps words to an integer, returns integer if it already exists in the dictionary
		if word in word_map:
			return word_map[word];

		word_index = len(word_list)
		word_list.append(word)
		word_map[word] = word_index
		
		return word_index
		
	for message in user_messages: # converts words into lists of integers
		new_message = message.split()
		message_to_ints = []
		
		for word in new_message:
			message_to_ints.append(get_number(word))
			
		user_ints.append(numpy.array(message_to_ints, dtype = int))
			
	#print(user_ints)
				
client.run(TOKEN_AUTH)