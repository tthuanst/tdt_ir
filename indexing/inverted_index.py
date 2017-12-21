#!/usr/bin/env python

#
# Author: Hieu
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

#from stokenize import stokenize
import os,re

def indexing_basic(collections):
    #Do indexing ...
    indexed_data = {}
    files = [os.path.join(collections,f) for f in os.listdir(collections)]
    for f in files:
        lines = open(f).readlines()
        f = os.path.basename(f)
        for line in lines:
            words = stokenize.stokenize_stop(line)
            for w in words:
                if indexed_data.has_key(w):
                    indexed_data[w].add(f)
                else:
                    indexed_data[w] = set([f])
    return indexed_data

def indexing_TF_IDF(collections):
    #Do indexing ...
    indexed_data = {}
    indexTF = 0
    indexIDF = 1
    countDoc = 0
    files = [os.path.join(collections,f) for f in os.listdir(collections)]
    for f in files:
        lines = open(f).readlines()
        f = os.path.basename(f)
        N = N + 1
        for line in lines:
            words = stokenize.stokenize_stop(line)
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
    return N,indexed_data

def indexing_boolean(collections):
    #Do indexing ...
    indexed_data = {}   # key+value
    indexed_data['__doc_list__'] = []  #list
    files = [os.path.join(collections,f) for f in os.listdir(collections)]
    for f in files:
        f = os.path.basename(f)
        indexed_data['__doc_list__'].append(f)
    for f in files:
        lines = open(f).readlines()
        f = os.path.basename(f)
        for line in lines:
            #words = stokenize.stokenize_stop(line)
            for w in line.split():
                if not indexed_data.has_key(w):
                    indexed_data[w] = []
                    for d in indexed_data['__doc_list__']:
                        if d == f:
                            indexed_data[w].append(True)
                        else:
                            indexed_data[w].append(False)
                else:
                    indexed_data[w][indexed_data['__doc_list__'].index(f)] = True
    return indexed_data



if __name__ == '__main__':
    dict_data = indexing_boolean("/home/thanh/Desktop/tdt_ir/collections/ohsumed-all-docs")
    #print(dict_data['hyperbaric'])
    for i in range(len(dict_data['__doc_list__'])):
        if dict_data['hyperbaric'][i] and dict_data['oxygen'][i]:
            print(dict_data['__doc_list__'][i])
    #print(dict_data["hello"])