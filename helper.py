import numpy

running = False

idle_status = "with nothing (!~help)"
active_status = "with someone's data (please wait!)"

word_map = {"<PAD>": 0} # map padding to 0 by default

def get_number(word):
	"""Returns an integer mapping a word to an index and adds it in the dictionary if it did not already exist"""
	if word in word_map:
		return word_map[word];

	word_index = len(word_map)
	word_map[word] = word_index
		
	return word_index
	
def messages_to_ints(messages):
	"""Converts words into lists of integers"""
	ints = []

	for message in messages: 
		new_message = message.split()
		converted_message = []
	
		for word in new_message:
			converted_message.append(get_number(word))
			
		ints.append(numpy.array(converted_message, dtype = int))
		
	return ints
	
def reduce_nest(nested_arrays):
	"""Returns a 1D list of data based on nested arrays"""
	count = 0
	sum = 0
	for val_array in nested_arrays: # reduces nested arrays of different size into one float
		if len(val_array) > 0:
			sum += val_array[0]
			count += 1
			
	if count > 0:
		return sum / count
	else:
		return 0