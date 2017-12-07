#!/usr/bin/env python

#
# Author: Tran Thuan - 166005004
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

import os,re,math
from stokenize import stokenize
from collections import Counter

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

def indexing_2(collections):
    #Do indexing ...
    indexed_data = {}
    indexed_data['__countDoc__'] = 0
    files = [os.path.join(collections,f) for f in os.listdir(collections)]
    for f in files:
        lines = open(f).readlines()
        f = os.path.basename(f)
        #Counting number of document in collections
        indexed_data['__countDoc__'] = indexed_data['__countDoc__'] + 1
        for line in lines:
            for w in stokenize.stokenize_stop(line):
                if indexed_data.has_key(w):
                    #Count term w in document f
                    if indexed_data[w].has_key(f):
                        indexed_data[w][f] = indexed_data[w][f] + 1
                    else:
                        indexed_data[w][f] = 1
                else:
                    #Create dict with key(f) for term w
                    indexed_data[w] = dict()
                    indexed_data[w][f] = 1
    return indexed_data

def rank_search(query,indexed_data):
    result = None
    for w in query:
        if indexed_data.has_key(w):
            if result is None:
                result = set(indexed_data[w].keys())
            else:
                #Union 2 set of doc names
                result = result | set(indexed_data[w].keys())
    score = {}
    if result is not None:
        for d in result:
            for t in query:
                if indexed_data[t].has_key(d):
                    #Calculate weight for term in doc
                    tf = indexed_data[t][d]
                    idf = indexed_data['__countDoc__']/len(indexed_data[t].keys())
                    weight = (1+math.log10(tf))*(math.log10(idf))
                    if score.has_key(d):
                        score[d] = score[d] + weight
                    else:
                        score[d] = weight
        #Get top 10 highest score
        result = Counter(score)
        return result.most_common(10)
    else:
        #For pretty printout
        return set(["Not found"])

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
