#/usr/bin/python
# -*- coding: utf-8 -*-

"""
Natural Language Processing homework assignment.
Valentin Lemière - Guillaume Desquesnes
"""

import codecs
import collections
import sys

from Config import Config

class Corpus (object):
	"""
	A corpus of documents.
	Représente un corpus de documentss.
	"""
	
	def __init__ (self, documents, termino):
		"""
		Constructor.
		
		@param documents The list of documents.
		@param termino Corpus terminology, can be None.
		"""
		
		self.documents = documents
		self.nb_docs = len(documents)
		self.termino = termino
		self.config = Config()
		
	def preprocess (self):
		"""
		Launch the preprocess of each document, compute statistics for the G2 calculations.
		"""
		
		termino = self.termino != None
		
		# Number of occurence of each word in the corpus
		self.words = collections.defaultdict(int)
		
		for i in xrange(self.nb_docs):
			name = self.documents[i].f
			sys.stdout.write( "\r%3i/%i %s"%( i+1, self.nb_docs, '{:<70}'.format(name) ) )
			sys.stdout.flush()
			
			self.documents[i].preprocess(self.words, termino)
			
		# Number of words in the corpus
		self.size = sum(self.words.values())
		
	def process (self):
		"""
		Launch the keywords extraction and scoring in each document.
		"""
		
		for i in xrange(self.nb_docs):
			name = self.documents[i].f
			sys.stdout.write( "\r%3i/%i %s"%( i+1, self.nb_docs, '{:<70}'.format(name) ) )
			sys.stdout.flush()
			
			self.documents[i].process(self, self.termino)
			
			if self.config.testing and not self.config.nostats:
				self.documents[i].score()
		
	def results (self):
		"""
		Compute the score of the corpus.
		"""
		
		if self.config.nostats:
			print "One or more documents have no keywords, statistics are unavailable."
			return
		
		avg_nb_keyword = sum([doc.nb_extracted_keywords for doc in self.documents]) / float(self.nb_docs)
		
		if self.config.macro_average:
			avg_precision = sum([doc.precision for doc in self.documents]) / self.nb_docs
			avg_recall = sum([doc.recall for doc in self.documents]) / self.nb_docs
			avg_f1 = sum([doc.f1 for doc in self.documents]) / self.nb_docs
		else:
			good = sum([doc.good for doc in self.documents])
			nb_extracted_keywords = sum([doc.nb_extracted_keywords for doc in self.documents])
			nb_keywords = sum([doc.nb_keywords for doc in self.documents])
			
			avg_precision = good / nb_extracted_keywords
			avg_recall = good / nb_keywords
			avg_f1 = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall) if (avg_precision + avg_recall) != 0 else 0
		
		print "Keywords   : %4.2f"%avg_nb_keyword
		print "Precision  : %4.2f"%avg_precision
		print "Recall     : %4.2f"%avg_recall
		print "F1 score   : %4.2f"%avg_f1

	def save (self, f):
		"""
		Save the extracted keywords in a file.
		
		@param f File to write into.
		"""
		
		with codecs.open(f, 'w', "UTF-8") as f:
			for doc in self.documents:
				f.write("%s\t%s\n"%(doc.f[doc.f.rindex("/")+1:], ";".join(doc.extracted_keywords)))

