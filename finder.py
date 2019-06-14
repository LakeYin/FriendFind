import discord
import helper
import numpy
numpy.random.seed(9999)

import tensorflow
from tensorflow import keras

async def find_friends(user, guild):
	"""Returns a dictionary of floats representing similarity percentage mapped to Discord user mentions based on the user and guild"""
	user_messages, other_messages = await helper.gather_messages(user, guild)
	
	other_messages = dict((id, messages) for (id, messages) in other_messages.items() if len(messages) >= 10)
	
	user_ints = []
	other_ints = {}
	
	user_ints = helper.messages_to_ints(user_messages)
	user_ints = keras.preprocessing.sequence.pad_sequences(user_ints, value = helper.word_map["<PAD>"], padding = "post", maxlen = 2000) # max character count for a discord message is 2000
	
	for id, messages in other_messages.items():
		other_ints[id] = helper.messages_to_ints(messages)
	
	labels = numpy.array([1] * len(user_ints), dtype=int)
	#print(user_ints)
	
	epochs = max(10, 30 - int(len(labels) / 100))
	
	model = create_model(len(helper.word_map))
	print("Fitting model")
	model.fit(user_ints, labels, epochs = epochs, verbose = 1)
	
	print("Making predictions")
	
	return await make_predictions(other_ints, model)
		
def create_model(vocab):
	"""Returns a Keras model based on the size of the vocabulary and other settings"""
	model = keras.Sequential()
	model.add(keras.layers.Embedding(vocab, 16))
	model.add(keras.layers.GlobalAveragePooling1D())
	model.add(keras.layers.Dense(16, activation=tensorflow.nn.relu))
	model.add(keras.layers.Dense(1, activation=tensorflow.nn.sigmoid))
	
	model.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["acc"])
	
	return model

async def make_predictions(users_ints, model):	
	"""Returns a dictionary of predictions based on a dictionary of user messages converted to numpy int arrays and a Keras model"""
	predictions = {}
	
	for id, ints in users_ints.items():
		sum, count = 0, 0
		for int_message in ints: 
			prediction = helper.reduce_nest(model.predict(int_message))
			if prediction > 0:
				count += 1
				sum += prediction
		
		if count > 0:
			predictions[id] = sum / count
		else:
			predictions[id] = 0
		
	return predictions
	
def clear_words():
	"""Clears the dictionary of word indexes"""
	helper.word_map.clear()