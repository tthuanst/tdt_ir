#!/usr/bin/env python

#
# Author: Tran Thuan - 166005004
# Project: Information Retrieval
# TDT University - Information Retrieval course
# Lecturer: Le Anh Cuong
#

import os,re

def indexing(collections):
    vocabulary = set()
    indexed_data = {}
    files = [os.path.join(collections,f) for f in os.listdir(collections)]
    for f in files:
        lines = open(f).readlines()
        f = os.path.basename(f)
        for line in lines:
            for w in line.split():
                w = re.sub(r'/.*','',w)
                vocabulary.add(w)
                if indexed_data.has_key(w):
                    indexed_data[w].add(f)
                else:
                    indexed_data[w] = set([f])
    return indexed_data

def search(ids,indexed_data):
    result = None
    #for i in ids:
    for i in ids.split():
        if indexed_data.has_key(i):
            if result is None:
                result = set(indexed_data[i])
            else:
                result = result & set(indexed_data[i])
    if result is None or len(result) == 0:
        return set(["Not found"])
    else:
        return result


if __name__ == '__main__':
    print("Test done by ir_main.py")
