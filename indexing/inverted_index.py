#!/usr/bin/env python

#
# Author: Hieu
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

from stokenize import stokenize
import os,re

example_output = {
                    1: ["doc1","doc5","doc10"],
                    2: ["doc2","doc5","doc9"]
                 }

def hashing(word):
    if word == "hello":
        hashnum = 1 #example
    elif word == "world":
        hashnum = 2 #example
    else:
        hashnum = 0 #example
    return hashnum

def indexing_basic(collections):
    #Do indexing ...
	vocabulary = set()
	indexed_data = {}
	files = [os.path.join(collections,f) for f in os.listdir(collections)]
	for f in files:
		lines = open(f).readlines()
		f = os.path.basename(f)
		for line in lines:
			words = stokenize.stokenize(line)
			for w in words:
				if indexed_data.has_key(w):
					indexed_data[w].add(f)
				else:
					indexed_data[w] = set([f])
					vocabulary.add(w)
	return indexed_data
	
def indexing_TF_IDF(collections):
    #Do indexing ...
	vocabulary = set()
	indexed_data = {}
	indexTF = 0
	indexIDF = 1
	files = [os.path.join(collections,f) for f in os.listdir(collections)]
	for f in files:
		lines = open(f).readlines()
		f = os.path.basename(f)
		for line in lines:
			words = stokenize.stokenize(line)
			for w in words:
				if w in indexed_data:
					indexed_data[w][indexIDF].add(f)
					if f in indexed_data[w][indexTF]:
						indexed_data[w][indexTF][f] = indexed_data[w][indexTF][f] + 1
					else:
						indexed_data[w][indexTF] = {}
						indexed_data[w][indexTF][f] = 1
				else:
					indexed_data[w] = {}
					indexed_data[w][indexTF] = {}
					indexed_data[w][indexTF][f] = 1
					indexed_data[w][indexIDF] = set([f])
					vocabulary.add(w)
	return indexed_data


if __name__ == '__main__':
    #For test: ./inverted_index.py
    dict_data = indexing("../collections")
    print(dict_data[hashing("hello")])