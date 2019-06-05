import numpy

running = False

word_list = []
word_map = {}

def get_number(word): # maps words to an integer, returns integer if it already exists in the dictionary
	if word in word_map:
		return word_map[word];

	word_index = len(word_list)
	word_list.append(word)
	word_map[word] = word_index
		
	return word_index
	
def messages_to_ints(user_messages): # converts words into lists of integers
	ints = []

	for message in user_messages: 
		new_message = message.split()
		converted_message = []
	
		for word in new_message:
			converted_message.append(get_number(word))
			
		ints.append(numpy.array(converted_message, dtype = int))
		
	return ints