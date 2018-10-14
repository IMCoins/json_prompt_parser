	# def list_decrypt(self, data, mapping, depth):
	# 	"""
	# 		self.seeking_tree == True
	# 	"""

	# 	#	If we want to fill a premade mapping, we will follow only one dict,
	# 	#	the first, and only one.

	# 	# 	Since the mapping contains only a list of one element, showing us the way for
	# 	#	the entirety of the list, we only have the [0] index to iterate on.
	# 	if self.seeking:
	# 		mapping = mapping[0]

	# 	data_arr = []
	# 	for data_item in data:
	# 		curr_map = {}
	# 		for key, value in mapping.items():
	# 			if key in data_item:
	# 				curr_map[key] = self.data_parser(key, value, data_item)

	# 		data_arr.append( curr_map )
	# 	return data_arr

	# def dict_decrypt(self, data, mapping, depth)
	# 	for key, value in mapping:
	# 		if key in data:
	# 			pass

	# def decrypt(self, verbose=False):
	# 	if self.jsonfile == None:
	# 		raise ValueError("No file has already been loaded. Please, look at .load() method.")

	# 	self.map_as_string = ''
	# 	self.curr_map = {}
	# 	for key, value in self.jsonfile.items():
	# 		self.curr_map[key] = self.data_parser(jsonfile, key, value)

	# 	if verbose:
	# 		print(self.map_as_string)
		# return None

import json

class Json_mapping():
	"""	This classes will parse and make it easy to read for the human eye on a mere prompt.
		It has originally been designed for inventory purposes of huge json databases.
	"""
	def __init__(self, verbose=False):
		"""	Args:
				verbose: bool
					Decides whether or not to print the variables that are not json Data Structures.
			Returns:
				None, this is the __init__ method.
		"""
		self.jsonfile = None

		#	Settings
		self.repr = verbose

	def format_data(self, v):
		"""	Args:
				v: any python obj with __repr__ nicely defined
			Returns:
				If verbose is true via self.repr attribute, return the variable.
				Else return its type.
		"""
		if self.repr:
			if isinstance(v, dict) or isinstance(v, list):
				#	Commenting as this line includes a more condensed data summary.
				return '// {}'.format(v)
			else:
				return v
		return type(v)

	def decrypt(self, data=None, depth=0):
		"""	Args:
				data: dict
					Data to store in message to print or to put in file.
				depth: int
					Literally depth of our recursive call. Decides how many \\t to print.
		"""
		#	Helper for first function call.
		#	To be deleted in a better version.
		if data is None:
			data = self.jsonfile

		mess = ""
		for k, v in data.items():
			mess += "{}{} : {}\n".format(depth * '\t', k, self.format_data(v))
			if isinstance(v, dict):
				mess += self.decrypt(v, depth + 1)
			elif isinstance(v, list) and len(v) > 0:
				mess += self.decrypt(v[0], depth + 1)
		self.map_as_string = mess
		return mess

	def data_parser(self, key, value, data, depth):
		if self.repr:
			print( "{}{} : {}\n".format(depth * '\t', key, self.format_data(value)), end='')

		if isinstance(value, dict):
			return self.get_data_from_map(value, data[key], depth + 1)
		elif isinstance(value, list):
			return self.get_arr_from_map(value, data[key], depth + 1)

		return data[key]

	def get_arr_from_map(self, mapping, data, depth):
		"""	Args:
				mapping:dict
					Originally a json converted to dict that precisely tells us which data
					do we want to collect.
				data:list
					Array to iterate on to collect each dictionnary inside it.
			Returns:
				Array of dictionnary.
		"""
		data_arr = []
		for data_item in data:
			curr_map = {}
			# 	Since the mapping contains only a list of one element, showing us the way for
			#	the entirety of the list, we only have the [0] index to iterate on.
			for key, value in mapping[0].items():
				if key in data_item:
					curr_map[key] = self.data_parser(key, value, data_item, depth)

			data_arr.append( curr_map )
		return data_arr

	def get_data_from_map(self, mapping=None, data=None, depth=0):
		"""	Args:
				mapping: dict
					Originally a json converted to dict that precisely tells us which data
					do we want to collect.
				data: dict
					Data to collect from.
			Returns:
				Dictionnary which contains the filled data in mapping from data.
		"""
		#	Helper for first function call.
		#	To be deleted in a better version.
		if data is None:
			data = self.jsonfile
		if mapping is None:
			mapping = self.mapping

		curr_map = {}
		#	As this takes care of the dict case, iterating through the mapping first
		#	saves us computation time running through our tree.
		for key, value in mapping.items():
			if key in data:
				curr_map[key] = self.data_parser(key, value, data, 0)

		return curr_map

	def to_file(self, out = 'default.map'):
		"""	Args:
				out: path
					Path in which to put the json that has been previously read
			Returns:
				None
		"""
		if not out.endswith('.map'):
			out += '.map'

		try:
			with open(out, "w") as outfile:
				outfile.write(self.map_as_string)
		except AttributeError:
			print("Can't write to file since decrypt hasn't been computed yet.")

	def load(self, filename):
		with open(filename, "r") as f:
			jsonfile = json.loads( ''.join(f.readlines()) )
		
		self.jsonfile = jsonfile
		return self.jsonfile

	def load_map(self, filename):
		with open(filename, "r") as f:
			jsonfile = json.loads( ''.join( f.readlines()) )
		self.mapping = jsonfile
		return self.mapping

if __name__ == '__main__':
	#	Current architecture from json, to dict, to humanly readable file.
	json_map = Json_mapping(verbose=True)
	json_map.load('vpods_2.json')
	json_map.decrypt()
	json_map.to_file("vpods_2.map")

	json_map.load_map('map.json')
	filled_map = json_map.get_data_from_map()
	print(filled_map)
	# json_map.map_to_file("map.map")
	# print(filled_map)