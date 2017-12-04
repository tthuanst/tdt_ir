#!/usr/bin/env python

#
# Author: Phi
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

import nltk

example_vob = ["hello","world"]

def build_vocabulary(collections):
    #Find all files in folder path collections
    #Read each file and add new word to vocabulary
    return example_vob

def stokenize(sentence):
    #Not need change this function now
	
    return nltk.word_tokenize(sentence)


if __name__ == '__main__':
    #For test: ./stokenize.py
    print(build_vocabulary("../collections"))