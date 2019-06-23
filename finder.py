import discord
import helper
import numpy
numpy.random.seed(9999)

import tensorflow
from tensorflow import keras

async def find_friends(user, guild, dictionary):
	"""
	Creates dictionary of floats representing similarity percentage mapped to Discord user mentions based on the user and guild
	
	Arguments:
		user (User): The target Discord user
		guild (Guild): The Discord server the user belongs to
		dictionary (Dictionary): The dictionary to reference words as ints
	"""
	user_messages, other_messages = await helper.gather_messages(user, guild)
	
	other_messages = dict((id, messages) for (id, messages) in other_messages.items() if len(messages) >= 10)
	
	user_ints = []
	other_ints = {}
	
	user_ints = dictionary.messages_to_ints(user_messages)
	user_ints = keras.preprocessing.sequence.pad_sequences(user_ints, value = dictionary.get_number("<PAD>"), padding = "post", maxlen = 2000) # max character count for a discord message is 2000
	
	for id, messages in other_messages.items():
		other_ints[id] = dictionary.messages_to_ints(messages)
	
	labels = numpy.array([1] * len(user_ints), dtype=int)
	#print(user_ints)
	
	epochs = max(10, 30 - int(len(labels) / 100))
	
	model = create_model(len(dictionary.word_map))
	print("Fitting model")
	model.fit(user_ints, labels, epochs = epochs, verbose = 1)
	
	print("Making predictions")
	
	return await make_predictions(other_ints, model)
		
def create_model(vocab):
	"""
	Creates a Keras model 
	
	Arguments:
		vocab (int): The size of the vocabulary
	"""
	model = keras.Sequential()
	model.add(keras.layers.Embedding(vocab, 16))
	model.add(keras.layers.GlobalAveragePooling1D())
	model.add(keras.layers.Dense(16, activation=tensorflow.nn.relu))
	model.add(keras.layers.Dense(1, activation=tensorflow.nn.sigmoid))
	
	model.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["acc"])
	
	return model

async def make_predictions(users_ints, model):	
	"""
	Creates a dictionary of predictions
	
	Arguments:
		user_ints ({int : [[int]]}): A dictionary of user messages converted to a list of numpy int arrays
		model (Model): The Keras model to make predictions
	"""
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