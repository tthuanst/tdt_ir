#!/usr/bin/env python

#
# Author: Tran Thuan - 166005004
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

import os,re,math
from stokenize import stokenize

def indexing(collections,indexed_data): #First draft in case of Hieu not yet done
    #Do indexing ...
    #vocabulary = set()
    count1 = 0
    count2 = 0
    if '__countDoc__' not in indexed_data.keys():
        indexed_data['__countDoc__'] = []
    #All document paths in collection
    files = [os.path.join(collections,f) for f in os.listdir(collections)]
    for f in files:
        lines = open(f).readlines()
        f = os.path.basename(f) #Get document name only
        if f in indexed_data['__countDoc__']:
            count1 = count1 + 1
            continue #Skip document already indexed
        indexed_data['__countDoc__'].append(f)
        count2 = count2 + 1
        for line in lines:
            #for w in stokenize.stokenize_stop(line):
            for w in line.split():
                #w = re.sub(r'/.*','',w) #This is for remove tag if use POS tagging data
                #vocabulary.add(w) #Build vocabulary, but it's not used
                if indexed_data.has_key(w):
                    #Add document name to posting list of dictionary term 'w'
                    indexed_data[w].add(f)
                else:
                    #Add first document name to posting list of dictionary term 'w'
                    indexed_data[w] = set([f])
    print("\tSkip %d files already indexed, index %d new files"%(count1,count2))
    return indexed_data

def indexing_2(collections,indexed_data):
    #Do indexing ...
    count1 = 0
    count2 = 0
    if '__countDoc__' not in indexed_data.keys():
        indexed_data['__countDoc__'] = {}
    files = [os.path.join(collections,f) for f in os.listdir(collections)]
    for f in files:
        lines = open(f).readlines()
        f = os.path.basename(f)
        if f in indexed_data['__countDoc__'].keys():
            count1 = count1 + 1
            continue #Skip document already indexed
        indexed_data['__countDoc__'][f] = 0
        count2 = count2 + 1
        for line in lines:
            #for w in stokenize.stokenize_stop(line):
            for w in line.split():
                indexed_data['__countDoc__'][f] = indexed_data['__countDoc__'][f]+1
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
    print("\tSkip %d files already indexed, index %d new files"%(count1,count2))
    return indexed_data

def vsm_search(query,indexed_data):
    score = rank_search(query,indexed_data)
    for d in score.keys():
        score[d] = score[d]/math.sqrt(indexed_data['__countDoc__'][d])
    return score

def indexing_position(collections,indexed_data):
    #Do indexing ...
    countIndexed = 0
    countIngdexing = 0
    indexWordInDoc = 0
    if '__countDoc__' not in indexed_data.keys():
        indexed_data['__countDoc__'] = []
    files = [os.path.join(collections,f) for f in os.listdir(collections)]
    for f in files:
        indexWordInDoc = 0
        lines = open(f).readlines()
        f = os.path.basename(f)
        if f in indexed_data['__countDoc__']:
            countIndexed = countIndexed + 1
            continue #Skip document already indexed
        indexed_data['__countDoc__'].append(f)
        countIngdexing = countIngdexing + 1
        for line in lines:
            #for w in stokenize.stokenize_stop(line):
            for w in line.split():
                indexWordInDoc = indexWordInDoc + 1
                if indexed_data.has_key(w):
                    #Count term w in document f
                    if not indexed_data[w].has_key(f):
                        indexed_data[w][f] = []
                    indexed_data[w][f].append(indexWordInDoc)
                else:
                    #Create dict with key(f) for term w
                    indexed_data[w] = dict()
                    indexed_data[w][f] = []
                    indexed_data[w][f].append(indexWordInDoc)
    print("\tSkip %d files already indexed, index %d new files"%(countIndexed,countIngdexing))
    return indexed_data

def rank_search(query,indexed_data):
    score = {}
    for t in query:
        if indexed_data.has_key(t):
            for d in indexed_data[t].keys():
                #Calculate weight for term in doc
                tf = indexed_data[t][d]
                idf = len(indexed_data['__countDoc__'])/len(indexed_data[t].keys())
                weight = (1+math.log10(tf))*(math.log10(idf))
                if score.has_key(d):
                    score[d] = score[d] + weight
                else:
                    score[d] = weight
    if len(score) != 0:
        return score
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

def phrase_search(query, indexed_data):
    result = set()
    candidates = set()
    candidatesTemp = set()
    for term in query:
        if indexed_data.has_key(term):
            if candidates is None or len(candidates) == 0:
                for doc in indexed_data[term]:
                    candidates.add(doc)
            else:
                candidatesTemp = set()
                for doc in indexed_data[term]:
                    candidatesTemp.add(doc)
                candidates = candidates & candidatesTemp
    if candidates is None or len(candidates) == 0:
        #For pretty printout
        return set(["Not found"])
    if len(query) > 1:
        for doc in candidates:
            for position in indexed_data[query[0]][doc]:
                for i in range(1, len(query)):
                    if not (position + i) in indexed_data[query[i]][doc] :
                        break
                    result.add(doc)
    else:
        result = candidates
    if len(result) != 0:
        return result
    else:
        #For pretty printout
        return set(["Not found"])

def phrase_rank_search(query, indexed_data):
    result = {}
    candidates = set()
    candidatesTemp = set()
    for term in query:
        if indexed_data.has_key(term):
            if candidates is None or len(candidates) == 0:
                for doc in indexed_data[term]:
                    candidates.add(doc)
            else:
                candidatesTemp = set()
                for doc in indexed_data[term]:
                    candidatesTemp.add(doc)
                candidates = candidates & candidatesTemp
    if candidates is None or len(candidates) == 0:
        #For pretty printout
        return set(["Not found"])
    if len(query) > 1:
        for doc in candidates:
            total_dis = 0
            for i in range(0,len(query)-1):
                min_dis = 999
                for p1 in indexed_data[query[i]][doc]:
                    for p2 in indexed_data[query[i+1]][doc]:
                        distance = math.fabs(p1-p2)
                        if min_dis > distance:
                            min_dis = distance
                total_dis = total_dis + min_dis
            score = 1.0/total_dis
            result[doc] = score
    else:
        result = candidates
    if len(result) != 0:
        return result
    else:
        #For pretty printout
        return set(["Not found"])

if __name__ == '__main__':
    print("Test done by ir_main.py")
