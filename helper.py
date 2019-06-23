import discord
import numpy
import logging

class Dictionary:
	def __init__(self):
		"""
		Creates a new empty dictionary with premapped padding
		"""
		self.word_map = {"<PAD>": 0} # map padding to 0 by default
		
	def get_number(self, word):
		"""
		Returns an integer mapping a word to an index and adds it in the dictionary if it did not already exist
		
		Arguments:
			word (string): The word to enter into the dictionary
		"""
		if word in self.word_map:
			return self.word_map[word];

		word_index = len(self.word_map)
		self.word_map[word] = word_index
		
		return word_index
		
	def messages_to_ints(self, messages):
		"""
		Converts words into lists of integers
	
		Arguments:
			messages (string[]): The list of messages
			dictionary (Dictionary): The dictionary to reference the words
		"""
		ints = []

		for message in messages: 
			new_message = message.split()
			converted_message = []
	
			for word in new_message:
				converted_message.append(self.get_number(word))
			
			ints.append(numpy.array(converted_message, dtype = int))
		
		return ints
	
	def clear_words(self):
		"""
		Clears the dictionary of word indexes
		"""
		self.word_map.clear()

async def gather_messages(user, guild):
	"""
	Returns a list of a user's messages and a dictionary mapping everyone else in a server's id to a list of their messages
	
	Arguments:
		user (User): The target Discord user
		guild (Guild): The Discord server the user belongs to
	"""
	user_messages = []
	other_messages = {}
	
	for member in guild.members:
		if not member.bot and not member == user:
			other_messages[member.id] = []
	
	for channel in guild.text_channels:
		try:
			async for message in channel.history(limit = 5000).filter(lambda m: not m.author.bot and not m.attachments): #filters out messages from bots and messages with attachments
				if message.author == user:
					user_messages.append(message.clean_content)
					
				elif message.author.id in other_messages:
					other_messages[message.author.id].append(message.clean_content)
			
			print("Recorded " + channel.name)
			
		except:
			print("Could not view " + channel.name)
			
	return user_messages, other_messages

	
def reduce_nest(nested_arrays):
	"""
	Returns a 1D list of data 
	
	Arguments:
		nested_arrays ([[int]]): The 2D array of integers to reduce
	"""
	count, sum = 0, 0
	for array in nested_arrays: # reduces nested arrays of different size into one float
		for value in array:
			sum += value
			count += 1
			
	if count > 0:
		return sum / count
	else:
		return 0

def create_embed(bot, user, report_count, ordered_list):
	"""
	Creates a Discord embed to send results to users
	
	Arguments:
		bot (User): The bot sending the embed
		user (User): The user recieving the embed
		report_count (int): The maximum number of entries in the embed
		ordered_list ({int, float}[]): An ordered list of tuples of Discord ids and their similarity score
	"""
	embed = discord.Embed(title = "Your top {} most similar people:".format(report_count))
	embed.set_author(name = user.name, icon_url = str(user.avatar_url))
	embed.set_footer(text = bot.name, icon_url = str(bot.avatar_url))
	
	i = 0
	while i < report_count and i < len(ordered_list):
		embed.add_field(name = create_progress_bar(20, ordered_list[i][1]) + " **{:.1%}**".format(ordered_list[i][1]), value = "<@{}>".format(ordered_list[i][0]), inline = False)
		i += 1
	
	return embed
	
def create_progress_bar(divisions, percentage):
	"""
	Creates a unicode progress bar
	
	Arguments:
		divisions (int): The total number of elements making up the progress bar
		percentage (float): The bar's percentage represented as a number between 0 and 1
	"""
	bar = "["
	
	for i in range(int(round(percentage * divisions))):
		bar += "█"
	
	for i in range(divisions - int(round(percentage * divisions))):
		bar += "▁"
	
	bar += "]"
	return bar
	
def create_logger():
	"""
	Creates a logging object
	"""
	logger = logging.getLogger("discord")
	logger.setLevel(logging.ERROR)
	handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
	handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
	logger.addHandler(handler)
	
	return logger
	