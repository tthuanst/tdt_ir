#!/usr/bin/env python

#
# Author: Phi
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

example_vob = ["hello","world"]

def build_vocabulary(collections):
    #Find all files in folder path collections
    #Read each file and add new word to vocabulary
    return example_vob

def stokenize(sentence):
    #Not need change this function now
	
    return nltk.word_tokenize(sentence)

def stokenize_stop(sentence):
	stop_words = set(stopwords.words('english'))
	stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
	list_of_words = [i.lower() for i in wordpunct_tokenize(sentence) if i.lower() not in stop_words]
	return list_of_words

if __name__ == '__main__':
    #For test: ./stokenize.py
    print(build_vocabulary("../collections"))