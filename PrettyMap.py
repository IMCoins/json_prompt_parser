import json

def file_writer(func):
	def wrapper(*args, **kwargs):
		decrypted_text = func(*args, **kwargs)
		if kwargs.get('filename'):
			with open(kwargs['filename'], 'w') as f:
				f.write(decrypted_text)
		return decrypted_text
	return wrapper

def format_text_from_iter(value):
	if isinstance(value, (list, dict, set)):# or isinstance(value, dict) or isinstance(value, set):
		return type(value)
	return value

def format_basic_value(value):
	if isinstance(value, str):
		return "'{}'".format(value)
	elif isinstance(value, int) or isinstance(value, float):
		return "{} ({})".format(value, type(value))

@file_writer
def decrypt(data, depth=0, max_iter=None, filename=None):
	message = ''
	if isinstance(data, (list, set)):# or isinstance(data, set):
		if depth == 0:
			#	We only increment the depth when meeting an iterable to display.
			#	But for the sake of user experience, we want to increment
			#	before displaying if we meet a list as first type.
			message += '{}{}:\n'.format(depth * '\t', type(data))
			depth += 1

		for count, item in enumerate(data):
			#	NOTE TO SELF : It could be a good idea to implement
			#	a feature that would give info on list components.
			if max_iter and max_iter <= count:
				break

			if isinstance(item, (list, set)):# or isinstance(item, set):
				#	The decrypt function in the else statement is not enough to take
				#	care about the nested lists to display.
				message += '{}{}:\n'.format(depth * '\t', format_text_from_iter(item))
				message += decrypt(item, depth + 1, max_iter)
			else:
				message += '{}{}---\n'.format(decrypt(item, depth, max_iter), depth * '\t')

	elif isinstance(data, dict):
		for key, item in data.items():
			message += '{}{} : {}\n'.format(depth * '\t', key, format_text_from_iter(item))
			if isinstance(item, (list, set, dict)):# or isinstance(item, dict) or isinstance(item, set):
				message += decrypt(item, depth + 1, max_iter)

	else:
		message = "{}{}\n".format(depth * '\t', format_basic_value(data) )

	return message

def load_json(file):
	with open(file, 'r') as f:
		return json.loads( ''.join( f.readlines() ) )

if __name__ == '__main__':
	#	Printing JSON
	data = load_json('vpods_2.json')
	# print( decrypt(data) )

	#	Printing... Python Objects !
	data = [
		{
			"First" : 1,
			"Second" : [
				["Lots", "of", 4, "elems"],
				4,
				"some_string",
				{
					'some_key' : {
						'some_other_key' : "I'll stop there for now"
					}
				}
			],
			"Third" : {"even some sets"}
		},
		{
			"First" : 2,
			"Second" : 2,
			"Third" : 4
		}
	]
	print( decrypt(data) )

	data = load_json('vpods.json')
	# print( decrypt(data, max_iter=1) )