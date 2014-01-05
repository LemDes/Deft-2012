#/usr/bin/python
# -*- coding: utf-8 -*-

"""
Natural Language Processing homework assignment.
Valentin Lemière - Guillaume Desquesnes
"""

import codecs

def load_terminology (path):
	"""
	Load the terminology list of words.
	
	@param path Path of the terminology file.
	
	@return A list containing the terminology.
	"""
	
	with codecs.open(path) as f:
		return [word.decode('UTF-8').strip() for word in f]
