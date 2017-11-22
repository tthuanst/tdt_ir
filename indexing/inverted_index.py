#!/usr/bin/env python

#
# Author: Hieu
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

from stokenize import stokenize

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

def indexing(collections):
    vob = stokenize.build_vocabulary(collections)
    #Do indexing ...
    return example_output


if __name__ == '__main__':
    #For test: ./inverted_index.py
    dict_data = indexing("../collections")
    print(dict_data[hashing("hello")])