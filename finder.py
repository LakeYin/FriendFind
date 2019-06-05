import discord
import helper
import numpy

async def find_friends(user, guild):
	user_messages = []
	other_messages = {}
	
	for member in guild.members:
		if not member.bot and not member == user:
			other_messages[member.id] = []
	
	for channel in guild.text_channels:
		try:
			async for message in channel.history().filter(lambda m: not m.author.bot and not m.attachments): #filters out messages from bots and messages with attachments
				if message.author == user:
					user_messages.append(message.clean_content)
					
				elif message.author.id in other_messages:
					other_messages[message.author.id].append(message.clean_content)
		
		except:
			print("Could not view " + channel.name)
				
	#print(user_messages)
	
	other_messages = dict((id, messages) for (id, messages) in other_messages.items() if len(messages) >= 10)
	#print(other_messages)
	
	user_ints = helper.messages_to_ints(user_messages)
	#print(user_ints)
	
def clear_words():
	helper.word_list.clear()
	helper.word_map.clear()