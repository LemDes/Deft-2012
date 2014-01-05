#/usr/bin/python
# -*- coding: utf-8 -*-

"""
Natural Language Processing homework assignment.
Valentin Lemière - Guillaume Desquesnes
"""

import collections
import nltk.collocations

from Config import Config

def bootstrap (otext):
	"""
	Returns the list of collocations in a text.
	
	@param otext The text to parse.
	
	@return The list of collocations found.
	"""
	
	# Make a copy of the text since it will be modified
	text = otext[:]
	
	s = len(text) - 1
	config = Config()
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	measures = [bigram_measures.dice, bigram_measures.pmi]
	
	for u in xrange(config.bootstrap_iteration):
		s, text = iteration(s, text, measures[u%2])
	
	return list_collocations(text)

def iteration (s, text, m):
	"""
	A bootstraping iteration.
	
	@param s The size of the text.
	@param text The text.
	@param m The measure to use.
	
	@return Tuple containing the new size and the modified text.
	"""
	
	config = Config()
	
	finder = nltk.collocations.BigramCollocationFinder.from_words(text)
	finder.apply_freq_filter(config.bootstrap_freq_filter)	
	bigrams = finder.nbest(m, config.boostrap_nb)
	
	# Find all bigrams occurences positions
	c = find_all(s, text, bigrams)

	# Bootstrap
	toDel, text = do_bootstraping(c, bigrams, text)
	
	# Remove all bigrams second words			
	text, s = clean(toDel, text, s)
	
	return s, text

def find_all (s, text, bigrams):
	"""
	Find all the positions of the bigrams.
	
	@param s The size of the text.
	@param text The text.
	@param bigrams The list of bigrams to look for.
	
	@return A dictionary with the bigrams as keys and the list of occurences as value.
	"""
	
	c = collections.defaultdict(list)
	t = 0
	
	# Using a dictionary to look up bigrams is faster.
	bg = dict.fromkeys(bigrams, True)
	
	while t < s:
		if text[t][-1] != ".":		
			o = (text[t],text[t+1])
			
			# If o is a valid bigram append the position
			if bg.has_key(o):
				c[o].append(t)
			
		t += 1
	
	return c
	
def do_bootstraping (c, bigrams, text):
	"""
	Bootstrap the bigrams.
	
	@param c The output from find_all.
	@param bigrams The list of bigrams to bootstrap.
	@param text The text.
	
	@return A tuple containing a list of empty words and the new text.
	"""
	
	toDel = []
	
	for b in bigrams:
		for x in c[b]:
			# If the bigram is still there
			if text[x] == b[0] and text[x+1] == b[1]:
				# Bootstrap
				text[x] = text[x] + "#" + text[x+1]
				# Empty the second word and flag it for removal
				text[x+1] = "#"
				toDel.append(x+1)
				
	return toDel, text
	
def clean (toDel, text, s):
	"""
	Remove all empty words generated from the bootstraping.
	
	@param toDel The list of the empty words positions.
	@param text The text.
	@param s The size of the text.
	
	@return A tuple containing the new text and its new size.
	"""
	
	# Each deleted word shifts the index by one
	dec = 0
	
	for x in sorted(toDel):
		del text[x-dec]
		dec += 1
		
	s -= dec
	
	return text, s
	
def list_collocations (text):
	"""
	Returns a list with all the collocations generated.
	
	@param text The text.
	
	@return A list of collocation.
	"""
	
	res = []
	
	for word in text:
		if '#' in word:
			res.append(word.replace("#", " "))
	
	return res
