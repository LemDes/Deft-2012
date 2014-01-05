#/usr/bin/python
# -*- coding: utf-8 -*-

"""
Natural Language Processing homework assignment.
Valentin Lemière - Guillaume Desquesnes
"""

import glob
import sys

from Config import Config
from Document import Document
from Corpus import Corpus
from Terminology import load_terminology

if "__main__" == __name__:
	config = Config()
	config.load("config.json")
	
	print "*******************************************"
	print "*                DEFT 2012                *"
	print "* Valentin Lemière - Guillaume Desquesnes *"
	print "*******************************************"
	
	files = glob.glob(config.corpus_path + "/*.xml")
	nb_files = len(files)
	
	# Terminology
	if config.termino_path == "":
		termino = None
	else:
		termino = load_terminology(config.termino_path)
		print "\nTerminology loaded"
	
	print "\nLoading %i files"%nb_files
	print "-------------------------------------------"
	
	docs = []
	
	# Load the files
	for i, f in enumerate(files):
		sys.stdout.write( "\r%3i/%i %s"%( i+1, nb_files, '{:<70}'.format(f) ) )
		sys.stdout.flush()
		docs.append(Document(f))
	
	corpus = Corpus(docs, termino)
	
	print "\n\nCorpus preprocessing"
	print "-------------------------------------------"
	corpus.preprocess()
	
	print "\n\nExtracting the keywords"
	print "-------------------------------------------"
	corpus.process()
	
	if Config().testing:
		print "\n\nResults (%s average)"%("Macro" if config.macro_average else "Micro")
		print "-------------------------------------------"
		corpus.results()
	else:
		print "\n"

	if config.save_file != "":
		print "\nResults saved in %s"%config.save_file
		corpus.save(config.save_file)
