import discord
import helper
import numpy
numpy.random.seed(9999)

import tensorflow
from tensorflow import keras

async def find_friends(user, guild):
	user_messages = []
	user_ints = []
	
	other_messages = {}
	other_ints = {}
	
	friend_values = {}
	
	for member in guild.members:
		if not member.bot and not member == user:
			other_messages[member.mention] = []
	
	for channel in guild.text_channels:
		try:
			async for message in channel.history(limit=5000).filter(lambda m: not m.author.bot and not m.attachments): #filters out messages from bots and messages with attachments
				if message.author == user:
					user_messages.append(message.clean_content)
					
				elif message.author.mention in other_messages:
					other_messages[message.author.mention].append(message.clean_content)
			
			print("Recorded " + channel.name)
			
		except:
			print("Could not view " + channel.name)
				
	#print(user_messages)
	
	other_messages = dict((mention, messages) for (mention, messages) in other_messages.items() if len(messages) >= 10)
	
	user_ints = helper.messages_to_ints(user_messages)
	user_ints = keras.preprocessing.sequence.pad_sequences(user_ints, value=helper.word_map["<PAD>"], padding='post', maxlen=2000) # max character count for a discord message is 2000
	
	for mention, messages in other_messages.items():
		other_ints[mention] = helper.messages_to_ints(messages)
	
	labels = numpy.array([1] * len(user_ints), dtype=int)
	#print(user_ints)
	
	model = create_model(len(helper.word_map))
	print("Fitting model")
	model.fit(user_ints, labels, epochs=30, verbose=0)
	
	print("Making predictions")
	for mention, ints in other_ints.items():
		total_value = 0
		count = 0
		for int_message in ints: 
			prediction = helper.reduce_nest(model.predict(int_message))
			if prediction > 0:
				count += 1
				total_value += prediction
			
		friend_values[mention] = total_value / count
	
	return friend_values
		
def create_model(vocab):
	model = keras.Sequential()
	model.add(keras.layers.Embedding(vocab, 16))
	model.add(keras.layers.GlobalAveragePooling1D())
	model.add(keras.layers.Dense(16, activation=tensorflow.nn.relu))
	model.add(keras.layers.Dense(1, activation=tensorflow.nn.sigmoid))
	
	model.compile(optimizer='adagrad', loss='binary_crossentropy', metrics=['acc'])
	
	return model	
	
def clear_words():
	helper.word_list.clear()
	helper.word_map.clear()