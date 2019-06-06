import discord
import helper
import numpy
import tensorflow
from tensorflow import keras

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
	
	user_ints = helper.messages_to_ints(user_messages)
	user_ints = keras.preprocessing.sequence.pad_sequences(user_ints, value=helper.word_map["<PAD>"], padding='post', maxlen=2000) # max character count for a discord message is 2000
	
	other_ints = {}
	for id, messages in other_messages.items():
		other_ints[id] = helper.messages_to_ints(messages)
	
	labels = numpy.array([1] * len(user_ints), dtype=int)
	#print(user_ints)
	
	model = create_model(len(helper.word_map))
	model.fit(user_ints, labels, epochs=40)
	
	for id, ints in other_ints.items():
		for int_message in ints:
			prediction = model.predict(int_message)
			print(str(id) + ":\n" + str(prediction))
	
def create_model(vocab):
	model = keras.Sequential()
	model.add(keras.layers.Embedding(vocab, 16))
	model.add(keras.layers.GlobalAveragePooling1D())
	model.add(keras.layers.Dense(16, activation=tensorflow.nn.relu))
	model.add(keras.layers.Dense(1, activation=tensorflow.nn.sigmoid))
	
	model.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['acc'])
	
	return model
	
def clear_words():
	helper.word_list.clear()
	helper.word_map.clear()