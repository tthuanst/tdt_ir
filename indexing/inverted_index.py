#
# Author: 
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

from stokenize import stokenize

example_output = {
					1: ["doc1","doc5","doc10"],
				  	2: ["doc2","doc5","doc9"]
				 }

def indexing(collections):
	vob = stokenize.build_vocabulary(collections)
	#Do indexing ...
	return example_output