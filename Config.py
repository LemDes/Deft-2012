#/usr/bin/python
# -*- coding: utf-8 -*-

"""
Natural Language Processing homework assignment.
Valentin Lemière - Guillaume Desquesnes
"""

import codecs
import json
import sys

class Config:
	"""
	The configuration of the application.
	Hold the value of the different parameters
	"""
	
	# Associate python type to full name.
	__types = { "unicode": "string", "str": "string", "int": "integer", "bool": "boolean", "float": "float" }
	
	# Default values of the config parameters.
	__shared_state = {
			"nostats": False,
			"corpus_path" : u"",
			"termino_path" : u"",
			"save_file" : u"res.txt",
			"size_min" : 4,
			"score_min" : 75,
			"score_min_termino" : 10,
			"freq_termino": 0.35,
			"freq_collocation": 6.0,
			"bootstrap_iteration": 3,
			"bootstrap_freq_filter": 4,
			"boostrap_nb": 200,
			"macro_average": True
			}


	def __init__(self):
		"""
		Constructor. Share the same state that other instance.
		"""

		self.__dict__ = self.__shared_state

	
	def load(self, filename):
		"""
		Load a configuration from a file.
	
		@param filename Name of the config file.
		"""

		try:	
			with codecs.open(filename, 'r',encoding="UTF-8") as f:
				data = json.loads(f.read())
				
				for attr,val in self.__dict__.items():
					if not attr in data:
						sys.stderr.write('Missing %s field. Using default value: %s\n'%(attr, str(self.__dict__[attr])))
					elif type(data[attr]) != type(val):
						sys.stderr.write('%s should be of type %s. Using default value: %s\n'%(attr, self.__types[type(val).__name__], str(self.__dict__[attr])))
					else:
						self.__dict__[attr] = data[attr]
		
		except IOError:
			sys.exit("%s does not exist or can't be read."%(filename))
		
		except ValueError:
			sys.exit("Encoding problem, encode the config file in UTF-8.")
