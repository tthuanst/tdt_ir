#!/usr/bin/env python

#
# Author: Tran Thuan - 166005004
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

import os,re

def indexing(collections): #First draft in case of Hieu not yet done
    vocabulary = set()
    indexed_data = {}
    #All document paths in collection
    files = [os.path.join(collections,f) for f in os.listdir(collections)]
    for f in files:
        lines = open(f).readlines()
        f = os.path.basename(f) #Get document name only
        for line in lines:
            for w in line.split(): #Simple stokenize, split by space
                w = re.sub(r'/.*','',w) #This is for remove tag if use POS tagging data
                vocabulary.add(w) #Build vocabulary, but it's not used
                if indexed_data.has_key(w):
                    #Add document name to posting list of dictionary term 'w'
                    indexed_data[w].add(f)
                else:
                    #Add first document name to posting list of dictionary term 'w'
                    indexed_data[w] = set([f])
    return indexed_data

def simple_search(query,indexed_data):
    result = None
    for w in query:
        if indexed_data.has_key(w):
            if result is None:
                #First set of doc names
                result = set(indexed_data[w])
            else:
                #Merge 2 set of doc names
                result = result & set(indexed_data[w])
    if result is None or len(result) == 0:
        #For pretty printout
        return set(["Not found"])
    else:
        #Set of doc names satisfy all terms of query
        return result


if __name__ == '__main__':
    print("Test done by ir_main.py")
