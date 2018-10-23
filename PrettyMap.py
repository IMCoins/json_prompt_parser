def format_text_from_dict(value):
	if isinstance(value, list):
		return ''
	return value

def format_text_from_arr(value):
	pass

def decrypt_dict(data, depth):
	message = ""
	for key, value in data.items():
		# message += '{}{} : {}\n'.format(depth * '\t', key, format_text_from_dict(value))
		message += decrypt(value, depth + 1)
	#	Going back into the parser
	return message

def decrypt_array(data, depth):
	message = ''
	for item in data:
		message += decrypt(item, depth + 1)
	#	Going back into the parser 
	return message

def decrypt(data, depth=0):
	if isinstance(data, list):
		message = '{}{} : {}\n'.format(depth * '\t', type(data), '')
		message += decrypt_array(data, depth)
		# Going into array_function with depth += 1
	elif isinstance(data, dict):
		# message = '{}{} :{}\n'.format(depth * '\t', type(data))
		message = decrypt_dict(data, depth + 1)
		# Going into dict_function with depth += 1
	else:
		message = '{}{}\n'.format(depth * '\t', data)
	return message

import json

def load_json(file):
	with open(file, 'r') as f:
		return json.loads( ''.join( f.readlines() ) )

if __name__ == '__main__':
	# print( decrypt('Hello') )
	# print()
	# print( decrypt({ 'values' : ['Hello', ['Hi', {'key' : 'value', 'key_2' : 'value_2'}], 3] }) )
	# print()
	data = load_json('vpods_2.json')
	print( decrypt(data) )
	# print( '\n\n\n' )
	# print( decrypt({'First key' : 2}))