#/usr/bin/python
# -*- coding: utf-8 -*-

"""
Natural Language Processing homework assignment.
Valentin Lemière - Guillaume Desquesnes
"""

import collections
import itertools
import math
from xml.dom import minidom

from nltk.tokenize.punkt import PunktWordTokenizer

from Bootstrap import bootstrap
from Config import Config

class Document (object):
	"""
	A document from a corpus.
	"""
	
	def __init__ (self, f):
		"""
		Constructor.
		
		@param f Name of the file containing the document.
		"""
		
		self.f = f
		self.content = []
		self.keywords = []
		self.extracted_keywords = []
		self.config = Config()
		xml = minidom.parse(f)
		
		# Parse the expected keywords
		keyword_tag = xml.getElementsByTagName("mots")
		if keyword_tag:
			self.config.testing = True
			
			for x in keyword_tag[0].childNodes:
				self.keywords = x.nodeValue.split(";")
		else:
			self.config.testing = False
			
		if len(self.keywords) == 0:
			self.config.nostats = True
		
		# Parse the summary
		for x in xml.getElementsByTagName("resume")[0].childNodes:
			if x.nodeName == "p" and x.childNodes:
				self.content.append(x.childNodes[0].nodeValue)
		
		# Parse the text
		for x in xml.getElementsByTagName("corps")[0].childNodes:
			if x.nodeName == "p" and x.childNodes:
				self.content.append(x.childNodes[0].nodeValue)
				
	def preprocess (self, words, termino):
		"""
		Tokenize the document and compute the statistics for the G2 calculation.
		
		@param words Global corpus counter containing for each word its occurence number.
		@param termino Boolean, will there be a terminology.
		"""
		
		# Tokenization
		tokens = []
		
		for text in self.content:
			tokens += PunktWordTokenizer().tokenize(text)
			
		self.content = tokens
		
		# Collocations
		if termino:
			self.collocations = []
		else:
			self.collocations = bootstrap(self.content)
		
		# Corpus statistics
		self.words = collections.defaultdict(int)
		stop = ['\'', '-', '`', '!', ':', ';', '.', ',']
		
		for word in self.content:
			if len(word) < self.config.size_min:
				continue
			
			if word[-1] in stop:
				word = word[:-1]
			if word[0] in stop:
				word = word[1:]
				
			if len(word) == 0:
				continue
			
			self.words[word] += 1 # Document counter
			words[word] += 1 # Corpus counter
			
		self.size = sum(self.words.values())
			
	def process (self, corpus, termino):
		"""
		Extract keywords from the document.
		
		@param corpus The corpus the document belongs in.
		@param termino The corpus terminology, if None won't be used.
		"""
		
		words_g2_score = []
		value_words = {}
		
		# Score each word with the G2
		for word in self.words:
			in_corpus = corpus.words[word] if corpus.words.has_key(word) else 0
			in_document = self.words[word] if self.words.has_key(word) else 0
			total = in_corpus + in_document
			
			e1 = ( corpus.size * total ) / float( corpus.size + self.size )
			e2 = ( self.size * total ) / float( corpus.size + self.size )
			
			if in_corpus / e1 == 0 or in_document / e2 == 0:
				continue
			
			j = in_corpus * math.log( in_corpus / e1 )
			k = in_document * math.log( in_document / e2 )
			
			g2 = 2 * (j + k)
					
			words_g2_score.append( (g2, word) )
			value_words[word] = g2
			
		# Keywords selection
		words_g2_score.sort(reverse=True)
		
		if not termino:
			words = [ g2_score[1] for g2_score in itertools.takewhile(lambda x: x[0] > self.config.score_min, words_g2_score) ]
			self.extracted_keywords = words
			self.terminology(self.collocations, words, value_words, False)
		else:
			words = [ g2_score[1] for g2_score in itertools.takewhile(lambda x: x[0] > self.config.score_min_termino, words_g2_score) ]
			self.terminology(termino, words, value_words, True)
			
		# Never no keywords
		if len(self.extracted_keywords) == 0:
			self.extracted_keywords.append(words_g2_score[0][1])
		
	def terminology (self, termino, words, value_words, isTermino):
		"""
		Add the terminology words susceptible to be keywords.
		
		@param termino The terminology to study.
		@param words List of potential keywords.
		@param value_words G2 score of each word.
		@param isTermino Boolean, true if terminology, false if collocation.
		"""
		
		# Using a dictionary to look up words is faster.
		words = dict.fromkeys(words, True)
		
		if isTermino:
			freq = self.config.freq_termino
		else:
			freq = self.config.freq_collocation
		
		for word_t in termino:
			score = 0
			tokens = PunktWordTokenizer().tokenize(word_t)
			
			# Count the number of word in the collocation which may be keywords.
			for word in tokens:
				if words.has_key(word):
					score += value_words[word]
			
			# If there is enough potential keywords in the collocation, add it
			if score >= freq * len(tokens) * self.config.score_min:
				self.extracted_keywords.append(word_t)
		
	def score (self):
		"""
		Compute the precision, recall and f1 score for the document.
		"""
		
		self.nb_keywords = len(self.keywords)
		
		# Don't count twice a same keyword
		found = [ 0.0 for x in xrange(self.nb_keywords) ]
		
		for e_kw in self.extracted_keywords:
			for x, kw in enumerate(self.keywords):
				if e_kw == kw:
					found[x] = 1.0
		
		self.good = sum(found)
		
		self.nb_extracted_keywords = len(self.extracted_keywords)
		self.precision = self.good / self.nb_extracted_keywords
		self.recall = self.good / self.nb_keywords
		self.f1 = 2 * (self.precision * self.recall) / (self.precision + self.recall) if (self.precision + self.recall) != 0 else 0
